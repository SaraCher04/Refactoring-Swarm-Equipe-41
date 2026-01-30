# src/agents/judge.py
import subprocess
import os
import sys
import time
import requests
from src.utils.logger import log_experiment, ActionType
from src.utils.tool import read_file, write_file

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def generate_tests_for_code(code: str, api_key: str, module_name: str) -> str:
    """
    Generate pytest-compatible unit tests for the given Python code.
    Returns the tests code string, or empty string on failure.
    Also logs the generation interaction.
    """
    input_prompt = (
        f"You are a Python QA engineer.\n"
        f"Please write valid pytest unit tests for the following Python code. Ensure the test functions start with `test_` and are written correctly to use pytest.\n"
        f"Make sure to include edge cases where relevant and avoid unnecessary assertions.\n"
        f"Return ONLY valid Python test code, no explanations or comments. Do not include any markdown or non-Python syntax.\n\n"
        f"Also, make sure that the import path matches the module structure, i.e. use `from {module_name} import factorial, fibonacci, power`.\n\n"
        f"{code}"
    )

    payload = {"contents": [{"parts": [{"text": input_prompt}]}]}

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.post(
                f"{GEMINI_URL}?key={api_key}", json=payload, timeout=120
            )
            if response.status_code == 200:
                tests_code = response.json()["candidates"][0]["content"]["parts"][0][
                    "text"
                ]
                tests_code = (
                    tests_code.replace("```python", "").replace("```", "").strip()
                )
                # Log successful generation
                log_experiment(
                    agent_name="JudgeAgent",
                    model_used="gemini-1.5-flash",
                    action=ActionType.GENERATION,
                    details={
                        "input_prompt": input_prompt,
                        "output_response": tests_code,
                    },
                    status="SUCCESS",
                )
                return tests_code
            else:
                # log failure response content
                log_experiment(
                    agent_name="JudgeAgent",
                    model_used="gemini-1.5-flash",
                    action=ActionType.GENERATION,
                    details={
                        "input_prompt": input_prompt,
                        "output_response": response.text,
                    },
                    status="FAILURE",
                )
        except requests.exceptions.RequestException as e:
            log_experiment(
                agent_name="JudgeAgent",
                model_used="gemini-1.5-flash",
                action=ActionType.DEBUG,
                details={"input_prompt": input_prompt, "output_response": str(e)},
                status="FAILURE",
            )
            if attempt == retries - 1:
                break
            time.sleep(5)

    return ""


def run_tests(
    code_file: str, api_key: str, module_name: str, generate_tests: bool = True
) -> tuple:
    """
    Run pytest for the target code file. If generate_tests is True, generate tests first.
    Returns (success: bool, feedback: str) where feedback is pytest output or error message.
    """
    directory = os.path.dirname(code_file)
    if directory not in sys.path:
        sys.path.insert(0, directory)

    test_file_path = code_file.replace(".py", "_test.py")

    if generate_tests:
        # Read codeee to send for test generation
        code = read_file(code_file)

        tests_code = generate_tests_for_code(code, api_key, module_name)
        if not tests_code:
            # Log generation failure (already logged inside generate_tests_for_code), return failure
            feedback = "Failed to generate pytest tests.."
            log_experiment(
                agent_name="JudgeAgent",
                model_used="gemini-1.5-flash",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": "Generate tests for code",
                    "output_response": feedback,
                },
                status="FAILURE",
            )
            return False, feedback

        # Write tests to file
        write_file(test_file_path, tests_code)

    else:
        # If not generating tests, make sure test file exists
        if not os.path.exists(test_file_path):
            feedback = "Test file not found; cannot re-run tests."
            log_experiment(
                agent_name="JudgeAgent",
                model_used="local",
                action=ActionType.DEBUG,
                details={
                    "input_prompt": "Check test file existence",
                    "output_response": feedback,
                },
                status="FAILURE",
            )
            return False, feedback

    # Run pytest on the test file
    result = subprocess.run(["pytest", test_file_path], capture_output=True, text=True)

    output = result.stdout + result.stderr
    status = "SUCCESS" if result.returncode == 0 else "FAILURE"

    # Log pytest execution (DEBUG)
    log_experiment(
        agent_name="JudgeAgent",
        model_used="local",
        action=ActionType.DEBUG,
        details={"input_prompt": "pytest execution", "output_response": output},
        status=status,
    )

    return result.returncode == 0, output
