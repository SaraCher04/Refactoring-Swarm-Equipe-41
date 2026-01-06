import subprocess
import requests
import time
from src.utils.logger import log_experiment, ActionType

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def run_tests(code_file: str, api_key: str) -> None:
    # Initialize status and tests_code before use
    status = "UNKNOWN"
    tests_code = ""

    with open(code_file, "r", encoding="utf-8") as f:
        code = f.read()

    input_prompt = (
        "You are a Python QA engineer.\n"
        "Please write valid pytest unit tests for the following Python code. "
        "Ensure the test functions start with `test_` and are written correctly to use pytest.\n"
        "Make sure to include edge cases where relevant and avoid unnecessary assertions.\n"
        "Return ONLY valid Python test code, no explanations or comments.\n\n"
        f"{code}"
    )

    payload = {
        "contents": [{"parts": [{"text": input_prompt}]}]
    }

    # Attempt to make a request to the Gemini API with retries for robustness
    retries = 3
    for attempt in range(retries):
        try:
            # Send request to Gemini API
            response = requests.post(
                f"{GEMINI_URL}?key={api_key}",
                json=payload,
                timeout=120  # Keep a long timeout to allow for detailed responses
            )

            # If the response is successful, exit the retry loop
            if response.status_code == 200:
                tests_code = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                status = "SUCCESS"
                break
        except requests.exceptions.RequestException as e:
            log_experiment(
                agent_name="JudgeAgent",
                model_used="gemini-1.5-flash",
                action=ActionType.DEBUG,
                details={"input_prompt": input_prompt, "output_response": str(e)},
                status="FAILURE"
            )
            status = "FAILURE"
            tests_code = ""
            if attempt < retries - 1:
                time.sleep(5)  # Retry after waiting 5 seconds
            else:
                raise  # Reraise after final attempt if still failing

    # Log the response from Gemini API
    if status == "SUCCESS":
        test_path = code_file.replace(".py", "_test.py")
        with open(test_path, "w", encoding="utf-8") as f:
            f.write(tests_code)

        # Run the generated tests using pytest
        result = subprocess.run(
            ["pytest", test_path],
            capture_output=True,
            text=True
        )

        log_experiment(
            agent_name="JudgeAgent",
            model_used="gemini-1.5-flash",
            action=ActionType.DEBUG,
            details={
                "input_prompt": input_prompt,
                "output_response": result.stdout + result.stderr
            },
            status="SUCCESS" if result.returncode == 0 else "FAILURE"
        )

    else:
        # Log failure if API response was not successful
        log_experiment(
            agent_name="JudgeAgent",
            model_used="gemini-1.5-flash",
            action=ActionType.DEBUG,
            details={"input_prompt": input_prompt, "output_response": "API request failed."},
            status="FAILURE"
        )
