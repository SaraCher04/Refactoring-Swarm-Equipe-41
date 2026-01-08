import re
from typing import Dict

def validate_prompt_quality(prompt: str, max_length: int = 5000) -> Dict:
    """
    Validates the quality of a system prompt for LLM agents.
    
    Checks include:
    - Presence of instructions/mission/objective
    - Presence of agent role
    - Minimum context length
    - Presence of output format and anti-hallucination instructions
    - Prompt length does not exceed max_length
    """
    # 1️⃣ Normaliser le texte
    text = prompt.lower()
    text = re.sub(r"\s+", " ", text)  # supprimer espaces multiples et sauts de ligne

    # 2️⃣ Vérifications
    checks = {
        "has_instruction": any(word in text for word in ["instruction", "mission", "objective", "task"]),
        "has_context": len(text.split()) > 20,  # au moins 20 mots pour avoir du contexte
        "has_agent_role": any(role in text for role in ["auditor", "fixer", "judge", "expert"]),
        "has_output_format": any(word in text for word in ["json", "report", "code", "summary"]),
        "has_anti_hallucination": any(word in text for word in ["avoid hallucination", "do not hallucinate", "focus only"]),
        "not_too_long": len(prompt) <= max_length,
    }

    return {
        "valid": all(checks.values()),
        "checks": checks,
        "length": len(prompt)
    }
