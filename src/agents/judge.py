import subprocess
import os
import sys
import requests  # <-- Add this import statement
from src.utils.logger import log_experiment, ActionType

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def generate_tests_for_code(code: str, api_key: str, module_name: str) -> str:
    """Generate pytest-compatible unit tests for the given Python code."""
    
    input_prompt = (
        f"You are a Python QA engineer.\n"
        f"Please write valid pytest unit tests for the following Python code. Ensure the test functions start with `test_` and are written correctly to use pytest.\n"
        f"Make sure to include edge cases where relevant and avoid unnecessary assertions.\n"
        f"Return ONLY valid Python test code, no explanations or comments. Do not include any markdown or non-Python syntax.\n\n"
        f"Also, make sure that the import path matches the module structure, i.e., use `from {module_name} import factorial, fibonacci, power`.\n\n"
        f"{code}"
    )

    payload = {
        "contents": [{"parts": [{"text": input_prompt}]}]
    }

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
                # Clean the response: remove markdown syntax like ```python and ```
                tests_code = tests_code.replace("```python", "").replace("```", "").strip()
                return tests_code
        except requests.exceptions.RequestException as e:
            log_experiment(
                agent_name="JudgeAgent",
                model_used="gemini-1.5-flash",
                action=ActionType.DEBUG,
                details={"input_prompt": input_prompt, "output_response": str(e)},
                status="FAILURE"
            )
            if attempt == retries - 1:
                raise  # Reraise after final attempt if still failing
            time.sleep(5)  # Retry after waiting 5 seconds

    return ""


def run_tests(code_file: str, api_key: str, module_name: str) -> None:
    """Generate and run tests on the provided Python code file."""
    
    # Step 1: Read the code from the file
    with open(code_file, "r", encoding="utf-8") as f:
        code = f.read()

    # Step 2: Generate the tests
    tests_code = generate_tests_for_code(code, api_key, module_name)

    if tests_code:
        # Step 3: Ensure the fixed file path is added to sys.path for imports
        directory = os.path.dirname(code_file)
        if directory not in sys.path:
            sys.path.insert(0, directory)

        # Step 4: Save the tests to a .py file
        test_file_path = code_file.replace(".py", "_test.py")
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(tests_code)

        # Step 5: Run the generated tests using pytest
        result = subprocess.run(
            ["pytest", test_file_path],
            capture_output=True,
            text=True
        )

        # Log the results of running the tests
        log_experiment(
            agent_name="JudgeAgent",
            model_used="gemini-1.5-flash",
            action=ActionType.DEBUG,
            details={
                "input_prompt": "Generated test execution",
                "output_response": result.stdout + result.stderr
            },
            status="SUCCESS" if result.returncode == 0 else "FAILURE",
        )

    else:
        # Log failure if test generation failed
        log_experiment(
            agent_name="JudgeAgent",
            model_used="gemini-1.5-flash",
            action=ActionType.DEBUG,
            details={"input_prompt": "Generate tests for code", "output_response": "Failed to generate tests."},
            status="FAILURE"
        )
