import os
import requests
from src.utils.logger import log_experiment, ActionType

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def analyze_code(code_file: str, api_key: str) -> list:
    with open(code_file, "r", encoding="utf-8") as f:
        code = f.read()

    input_prompt = (
        "You are a senior Python auditor.\n"
        "Analyze the following Python code and list concrete problems "
        "(bugs, bad practices, missing tests, missing docstrings).\n\n"
        f"{code}"
    )

    payload = {
        "contents": [{
            "parts": [{"text": input_prompt}]
        }]
    }

    response = requests.post(
        f"{GEMINI_URL}?key={api_key}",
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        output_response = response.text
        issues = ["Gemini API error during analysis"]
        status = "FAILURE"
    else:
        output_response = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        issues = [line.strip("- ") for line in output_response.splitlines() if line.strip()]
        status = "SUCCESS"

    log_experiment(
        agent_name="AuditorAgent",
        model_used="gemini-1.5-flash",
        action=ActionType.ANALYSIS,
        details={
            "input_prompt": input_prompt,
            "output_response": output_response,
            "issues_found": issues
        },
        status=status
    )

    return issues
