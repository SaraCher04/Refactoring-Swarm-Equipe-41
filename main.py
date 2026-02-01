# main.py
import argparse
import os
from dotenv import load_dotenv
from src.agents.auditor import analyze_code
from src.agents.fixer import fix_code
from src.agents.judge import run_tests
from src.utils.logger import log_experiment, ActionType
from src.utils.tool import validate_sandbox_path
from src.utils.tool import list_python_files
import subprocess
import re

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file (your .env key name)
API_KEY = os.getenv("GOOGLE_API_KEY")

# Ensure the API key is loaded
if not API_KEY:
    print(
        "❌ API_KEY not found in the environment variables. Please ensure it's set in the .env file."
    )
    exit(1)

MAX_FIXER_RETRIES = 3  # bounded to avoid infinite loops


def get_pylint_score(file_path: str) -> float:
    """Exécute pylint et retourne le score."""
    try:
        result = subprocess.run(
            ["pylint", file_path], capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        match = re.search(r"rated at ([\d\.]+)/10", output)
        if match:
            return float(match.group(1))
        else:
            return 0.0
    except Exception as e:
        print(f"⚠️ Pylint error: {e}")
        return 0.0


def process_file(file_path: str, api_key: str):
    """Process a single file through auditing, fixing, and testing with feedback loop."""
    print(f"🚀 Processing: {file_path}")

    # SAUVEGARDER le code original
    from src.utils.tool import read_file, write_file

    original_code = read_file(file_path)

    # 1. Vérifier Pylint initial
    score_before = get_pylint_score(file_path)
    print(f"📊 Pylint BEFORE: {score_before:.2f}/10")

    # Si code EXCELLENT (>9.0) ET tests existants ET passent → SKIP
    if score_before >= 9.0:
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        test_path = f"{file_path.replace('.py', '_test.py')}"

        if os.path.exists(test_path):
            success, _ = run_tests(
                file_path, api_key, module_name, generate_tests=False
            )
            if success:
                print(f"✅ Code already OPTIMAL! (Pylint: {score_before}, tests pass)")
                print(f"📈 No action needed")
                return

    # 2. Vérifier tests existants
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    test_path = f"{file_path.replace('.py', '_test.py')}"

    skip_test_generation = False

    if os.path.exists(test_path):
        success, feedback = run_tests(
            file_path, api_key, module_name, generate_tests=False
        )
        if success:
            print(f"✅ Existing tests PASS")
            skip_test_generation = True
        else:
            print(f"❌ Existing tests FAIL")
            skip_test_generation = False

    # 3. Auditor (toujours exécuté sauf si code optimal)
    print(f"🔍 Running auditor...")
    issues = analyze_code(file_path, api_key)

    if not issues or issues == ["Gemini API error during analysis"]:
        print(f"ℹ️  No issues found by auditor")

        # Si Pylint déjà bon ET tests passent → fin
        if score_before >= 8.0 and skip_test_generation:
            print(f"✅ Code already good enough")
            return

        issues = ["Code could use minor improvements"]  # Forcer une petite amélioration

    print(f"🔍 Auditor found {len(issues)} issues")
    for i, issue in enumerate(issues[:3], 1):  # Afficher 3 premières issues
        print(f"   {i}. {issue[:80]}...")
    if len(issues) > 3:
        print(f"   ... and {len(issues)-3} more")

    # 4. Fixer (UNE SEULE FOIS d'abord)
    print(f"🔧 Fixing issues...")
    fixed_file = fix_code(file_path, issues, api_key)

    # Vérifier qualité après fixing
    score_after_fix = get_pylint_score(fixed_file)
    print(f"📊 Pylint AFTER fix: {score_after_fix:.2f}/10")

    # Si qualité baisse BEAUCOUP, restaurer
    if score_after_fix < score_before - 1.0:
        print(f"⚠️  CRITICAL: Fixing DEGRADED quality significantly!")
        print(f"⚠️  Restoring original version...")
        write_file(fixed_file, original_code)
        score_after_fix = score_before
        fixed_file = file_path

    # 5. Tests finaux
    print(f"🧪 Running tests (generate: {not skip_test_generation})...")
    success, feedback = run_tests(
        fixed_file, api_key, module_name, generate_tests=not skip_test_generation
    )

    # UNE seule tentative de re-fix si échec
    if not success and MAX_FIXER_RETRIES > 0:
        print(f"❌ Tests failed, trying ONE re-fix with feedback...")
        # Limiter le feedback aux premières lignes
        short_feedback = "\n".join(feedback.split("\n")[:10])
        fixed_file = fix_code(
            fixed_file, issues, api_key, judge_feedback=short_feedback
        )

        # Re-tester
        success, feedback = run_tests(
            fixed_file, api_key, module_name, generate_tests=False
        )

    # 6. Résultats finaux
    score_final = get_pylint_score(fixed_file)
    improvement = score_final - score_before

    print(f"📊 Pylint FINAL: {score_final:.2f}/10")
    print(f"📈 Improvement: {improvement:+.2f}")

    if success:
        print(f"✅ SUCCESS: Tests pass + Quality improved!")
    else:
        print(f"❌ FAILED: Tests still fail")

    if improvement > 0:
        print(f"🎉 Quality IMPROVED!")
    elif improvement < 0:
        print(f"⚠️  Quality DECREASED!")
    else:
        print(f"➡️  Quality UNCHANGED")

    # Logging
    log_experiment(
        agent_name="QualityChecker",
        model_used="pylint",
        action=ActionType.ANALYSIS,
        details={
            "file": file_path,
            "score_before": score_before,
            "score_after": score_final,
            "improvement": improvement,
            "test_success": success,
            "input_prompt": f"Analyze {file_path}",
            "output_response": f"Before: {score_before}, After: {score_final}, Tests: {'PASS' if success else 'FAIL'}",
        },
        status="SUCCESS" if success else "FAILURE",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target_dir",
        type=str,
        required=True,
        help="Directory containing Python files to refactor",
    )
    args = parser.parse_args()

    target_dir = args.target_dir

    # Validate the path
    validate_sandbox_path(target_dir)

    # Process each Python file in the directory
    python_files = [
        f
        for f in list_python_files(target_dir)
        if not f.endswith("_test.py")  # Skip tests générés!
    ]
    for file_path in python_files:
        process_file(file_path, API_KEY)

    print("✅ Mission Complete")


if __name__ == "__main__":
    main()
