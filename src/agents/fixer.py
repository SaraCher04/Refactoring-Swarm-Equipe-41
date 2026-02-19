# src/agents/fixer.py
import requests
from src.utils.logger import log_experiment, ActionType
from src.utils.tool import read_file, write_file

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def fix_code(
    code_file: str, issues: list, api_key: str, judge_feedback: str = None
) -> str:
    code = read_file(code_file)
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

    input_prompt += (
        "Return ONLY the corrected Python code, no markdown, no backticks, nothing else.\n\n"
        f"{code}"
    )

    payload = {"contents": [{"parts": [{"text": input_prompt}]}]}

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={api_key}", json=payload, timeout=120
        )
    except requests.exceptions.RequestException as e:
        log_experiment(
            agent_name="FixerAgent",
            model_used="gemini-2.5-flash",
            action=ActionType.FIX,
            details={"input_prompt": input_prompt, "output_response": str(e)},
            status="FAILURE",
        )
        write_file(code_file, code)
        return code_file

    if response.status_code != 200:
        log_experiment(
            agent_name="FixerAgent",
            model_used="gemini-2.5-flash",
            action=ActionType.FIX,
            details={"input_prompt": input_prompt, "output_response": response.text},
            status="FAILURE",
        )
        write_file(code_file, code)
        return code_file

    # ✅ Strip fences BEFORE logging so log entry is also clean
    fixed_code = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    fixed_code = fixed_code.replace("```python", "").replace("```", "").strip()

    log_experiment(
        agent_name="FixerAgent",
        model_used="gemini-2.5-flash",
        action=ActionType.FIX,
        details={
            "input_prompt": input_prompt,
            "output_response": fixed_code,
        },  # ✅ log clean code
        status="SUCCESS",
    )

    write_file(code_file, fixed_code)
    return code_file
