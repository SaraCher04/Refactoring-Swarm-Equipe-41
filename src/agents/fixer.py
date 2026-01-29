import requests
from src.utils.logger import log_experiment, ActionType

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def fix_code(code_file: str, issues: list, api_key: str) -> str:
    with open(code_file, "r", encoding="utf-8") as f:
        code = f.read()

    input_prompt = (
        "You are a Python refactoring expert.\n"
        "Fix the following code based strictly on these issues:\n"
        f"{issues}\n\n"
        "Return ONLY the corrected Python code, nothing else.\n\n"
        f"{code}"
    )

    payload = {
        "contents": [{"parts": [{"text": input_prompt}]}]
    }

    response = requests.post(
        f"{GEMINI_URL}?key={api_key}",
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        output_response = response.text
        fixed_code = code  # If request fails, we return the original code
        status = "FAILURE"
    else:
        # Get the fixed code from the response
        fixed_code = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        output_response = fixed_code
        status = "SUCCESS"

        # Clean the generated code by removing unwanted markdown syntax
        fixed_code = fixed_code.replace("```python", "").replace("```", "").strip()

    # Save the fixed code to the original file
    with open(code_file, "w", encoding="utf-8") as f:
        f.write(fixed_code)

    # Log the fix process
    log_experiment(
        agent_name="FixerAgent",
        model_used="gemini-1.5-flash",
        action=ActionType.FIX,
        details={
            "input_prompt": input_prompt,
            "output_response": output_response
        },
        status=status
    )

    return code_file  # Return the path of the fixed file
