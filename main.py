# main.py
import argparse
import os
from dotenv import load_dotenv
from src.agents.auditor import analyze_code
from src.agents.fixer import fix_code
from src.agents.judge import run_tests
from src.utils.logger import log_experiment, ActionType

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file (your .env key name)
API_KEY = os.getenv("GEMINI_API_KEY")

# Ensure the API key is loaded
if not API_KEY:
    print("❌ API_KEY not found in the environment variables. Please ensure it's set in the .env file.")
    exit(1)

MAX_FIXER_RETRIES = 3  # bounded to avoid infinite loops

def process_file(file_path: str, api_key: str):
    """Process a single file through auditing, fixing, and testing with feedback loop."""
    print(f"🚀 Starting analysis for: {file_path}")

    # 1) Auditor
    refactoring_feedback = analyze_code(file_path, api_key)
    if not refactoring_feedback:
        print(f"❌ No issues found for {file_path}. Skipping.")
        return

    # 2) First fixing pass (based only on auditor issues)
    fixed_file_path = fix_code(file_path, refactoring_feedback, api_key)

    # 3) Judge: generate tests once and run them
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    success, feedback = run_tests(fixed_file_path, api_key, module_name, generate_tests=True)

    attempt = 1
    while not success and attempt <= MAX_FIXER_RETRIES:
        print(f"❌ Tests failed for {file_path}. Feedback: {feedback.splitlines()[0] if feedback else ''} Retrying ({attempt}/{MAX_FIXER_RETRIES})...")
        # Provide judge feedback to fixer so it can use the pytest output in the prompt
        fixed_file_path = fix_code(fixed_file_path, refactoring_feedback, api_key, judge_feedback=feedback)
        # Re-run tests but DO NOT regenerate tests (use already generated test file)
        success, feedback = run_tests(fixed_file_path, api_key, module_name, generate_tests=False)
        if success:
            print(f"✅ Tests passed for {file_path} after {attempt} retry(ies).")
            break
        attempt += 1

    if not success:
        print(f"❌ Maximum retries reached for {file_path}. Test failed.")
    else:
        print(f"✅ Finished successfully for {file_path}.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_dir", type=str, required=True, help="Directory containing Python files to refactor")
    args = parser.parse_args()

    target_dir = args.target_dir

    if not os.path.exists(target_dir):
        print(f"❌ Directory {target_dir} not found.")
        exit(1)

    # Process each Python file in the directory
    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)
        # Only process Python files (skip tests and other files)
        if os.path.isfile(file_path) and filename.endswith(".py") and not filename.endswith("_test.py"):
            process_file(file_path, API_KEY)

    print("✅ Mission Complete")

if __name__ == "__main__":
    main()
