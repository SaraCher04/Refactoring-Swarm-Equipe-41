# src/agents/auditor.py
import os
import requests
from src.utils.logger import log_experiment, ActionType
from src.utils.tool import read_file

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def analyze_code(code_file: str, api_key: str) -> list:
    """
    Read file, send audit prompt to LLM, log result and return parsed issues (list).
    """
    # read the fileee
    code = read_file(code_file)

    input_prompt = (
        "You are a senior Python auditor.\n"
        "Analyze the following Python code and list concrete problems (bugs, bad practices, missing tests, missing docstrings).\n\n"
        f"{code}"
    )

    payload = {"contents": [{"parts": [{"text": input_prompt}]}]}

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={api_key}", json=payload, timeout=120
        )
    except requests.exceptions.RequestException as e:
        output_response = str(e)
        issues = ["Gemini API error during analysis"]
        status = "FAILURE"
        # Mandatory logging of prompt + response per teacher's instruction
        log_experiment(
            agent_name="AuditorAgent",
            model_used="gemini-1.5-flash",
            action=ActionType.ANALYSIS,
            details={
                "input_prompt": input_prompt,
                "output_response": output_response,
                "issues_found": issues,
            },
            status=status,
        )
        return issues

    if response.status_code != 200:
        output_response = response.text
        issues = ["Gemini API error during analysis"]
        status = "FAILURE"
    else:
        output_response = response.json()["candidates"][0]["content"]["parts"][0][
            "text"
        ]
        # Keep parsing conservative: split lines, strip bullets
        issues = [
            line.strip(" -*•") for line in output_response.splitlines() if line.strip()
        ]
        status = "SUCCESS"

    log_experiment(
        agent_name="AuditorAgent",
        model_used="gemini-1.5-flash",
        action=ActionType.ANALYSIS,
        details={
            "input_prompt": input_prompt,
            "output_response": output_response,
            "issues_found": issues,
        },
        status=status,
    )

    return issues
