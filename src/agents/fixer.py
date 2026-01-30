# src/agents/fixer.py
import requests
from src.utils.logger import log_experiment, ActionType
from src.utils.tool import read_file, write_file

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def fix_code(
    code_file: str, issues: list, api_key: str, judge_feedback: str = None
) -> str:
    """
    Send refactoring prompt to LLM, optionally include judge feedback, save fixed code back to file.
    Returns path to the fixed file (same as input).
    """
    # read the fileee
    code = read_file(code_file)
    # Build prompt: include issues found and the judge feedback if present
    input_prompt = (
        "You are a Python refactoring expert.\n"
        "Fix the following code based strictly on these issues:\n"
        f"{issues}\n\n"
    )
    if judge_feedback:
        input_prompt += (
            "The tests failed with the following pytest output. Use this feedback to correct the code (do NOT regenerate tests):\n"
            f"{judge_feedback}\n\n"
        )

    input_prompt += "Return ONLY the corrected Python code, nothing else.\n\n" f"{code}"

    payload = {"contents": [{"parts": [{"text": input_prompt}]}]}

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={api_key}", json=payload, timeout=120
        )
    except requests.exceptions.RequestException as e:
        output_response = str(e)
        fixed_code = code  # fallback: keep original code
        status = "FAILURE"
        # Logging required fields
        log_experiment(
            agent_name="FixerAgent",
            model_used="gemini-1.5-flash",
            action=ActionType.FIX,
            details={"input_prompt": input_prompt, "output_response": output_response},
            status=status,
        )
        # Save (unchanged) to maintain consistency
        write_file(code_file, fixed_code)
        return code_file

    if response.status_code != 200:
        output_response = response.text
        fixed_code = code  # If request fails, return original code unchanged
        status = "FAILURE"
    else:
        fixed_code = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        output_response = fixed_code
        status = "SUCCESS"
        # Clean triple-backticks if any
        fixed_code = fixed_code.replace("```python", "").replace("```", "").strip()

    #  LOG ICI (pour SUCCESS et FAILURE)
    log_experiment(
        agent_name="FixerAgent",
        model_used="gemini-1.5-flash",
        action=ActionType.FIX,
        details={"input_prompt": input_prompt, "output_response": output_response},
        status=status,
    )

    # Sauvegarder le fichier
    write_file(code_file, fixed_code)

    return code_file
