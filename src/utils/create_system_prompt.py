from enum import Enum

class AgentType(str, Enum):
    AUDITOR = "auditor"
    FIXER = "fixer"
    JUDGE = "judge"

def create_system_prompt(agent_type: AgentType) -> str:
    """
    Creates a system prompt for each agent type.
    
    The prompt includes:
    - Agent role
    - Mission objectives
    - Expected output format
    - Instructions to avoid hallucinations
    """
    prompts = {
        AgentType.AUDITOR: (
            "SYSTEM INSTRUCTIONS:\n"
            "- You are an expert Python code auditor.\n"
            "- Your mission is to analyze the code without modifying it.\n"
            "- Identify bugs, PEP8 violations, and design a refactoring plan.\n"
            "- Return a structured audit report in JSON format including errors, warnings, and recommendations.\n"
            "- Always avoid hallucinations; focus only on the provided code."
        ),
        AgentType.FIXER: (
            "SYSTEM INSTRUCTIONS:\n"
            "- You are an expert Python code fixer.\n"
            "- Your mission is to correct the code according to the refactoring plan.\n"
            "- Fix only the identified bugs, respect PEP8, and add missing docstrings if needed.\n"
            "- Return the corrected code and a brief summary of changes.\n"
            "- Avoid introducing new bugs or hallucinations."
        ),
        AgentType.JUDGE: (
            "SYSTEM INSTRUCTIONS:\n"
            "- You are an expert Python testing agent.\n"
            "- Your mission is to execute unit tests and analyze the results.\n"
            "- Identify failures, their causes, and suggest corrections if necessary.\n"
            "- Return a structured test report in JSON format.\n"
            "- Focus only on the provided code and test outputs."
        ),
    }

    # Return the prompt for the agent, or a default system prompt if unknown
    return prompts.get(
        agent_type,
        "SYSTEM INSTRUCTIONS:\n- You are an AI assistant.\n- Follow the instructions carefully.\n- Avoid hallucinations."
    )
