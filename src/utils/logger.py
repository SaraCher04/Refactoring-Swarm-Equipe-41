import json
import os
import uuid
from datetime import datetime, timezone
from enum import Enum

# Chemin du fichier de logs
LOG_FILE = os.path.join("logs", "experiment_data.json")


class ActionType(str, Enum):
    """
    Énumération des types d'actions possibles pour standardiser l'analyse.
    (Agent-level semantics kept as Sara defined them)
    """
    ANALYSIS = "analysis"
    GENERATION = "generation"
    DEBUG = "debug"
    FIX = "fix"


# Data Officer: mapping agent-level actions -> experiment log contract actions
EXPERIMENT_ACTION_MAP = {
    "analysis": "CODE_ANALYSIS",
    "generation": "CODE_GEN",
    "debug": "DEBUG",
    "fix": "FIX",
}

def _strip_markdown_code_fences(text: str) -> str:
    """
    Remove surrounding Markdown code fences from a string, if present.
    Handles ```python ... ``` and ``` ... ``` cases.
    """
    if not isinstance(text, str):
        return text

    s = text.strip()

    if s.startswith("```"):
        lines = s.splitlines()
        # Remove first fence line (``` or ```python)
        if lines:
            lines = lines[1:]
        # Remove last fence line if present
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()

    return s
def log_experiment(agent_name: str, model_used: str, action, details: dict, status: str):
    """
    Enregistre une interaction d'agent pour l'analyse scientifique.

    Args:
        agent_name (str): Nom de l'agent (ex: "Auditor", "Fixer").
        model_used (str): Modèle LLM utilisé (ex: "gemini-1.5-flash").
        action: ActionType ou str (ex: ActionType.FIX, "fix", "FIX", "CODE_GEN", etc.).
        details (dict): DOIT contenir 'input_prompt' et 'output_response'.
        status (str): "SUCCESS" ou "FAILURE".

    Raises:
        ValueError: Si les champs obligatoires sont manquants dans 'details' ou si l'action/status est invalide.
    """

    # --- 0. VALIDATION STATUS ---
    if status not in ("SUCCESS", "FAILURE"):
        raise ValueError("❌ status doit être 'SUCCESS' ou 'FAILURE'.")

    # --- 1. VALIDATION + NORMALISATION DU TYPE D'ACTION ---
    valid_agent_actions = [a.value for a in ActionType]  # ["analysis","generation","debug","fix"]

    # Convert action to agent-level string
    if isinstance(action, ActionType):
        agent_action = action.value
    elif isinstance(action, str):
        agent_action = action.strip().lower()
        # Allow passing experiment-style strings too (optional convenience)
        reverse_map = {v.lower(): k for k, v in EXPERIMENT_ACTION_MAP.items()}
        agent_action = reverse_map.get(agent_action.lower(), agent_action)
    else:
        raise ValueError(
            f"❌ Action invalide : '{action}'. Utilisez ActionType (ex: ActionType.FIX) ou une string."
        )

    if agent_action not in valid_agent_actions:
        raise ValueError(
            f"❌ Action invalide : '{action}'. Actions agent autorisées: {valid_agent_actions}"
        )

    # Map to experiment contract action strings
    action_str = EXPERIMENT_ACTION_MAP.get(agent_action)
    if action_str is None:
        raise ValueError(f"❌ Action '{agent_action}' non mappée vers le contrat expérimental.")

    # --- 2.a VALIDATION STRICTE DES DONNÉES (Prompts) ---
    required_keys = ["input_prompt", "output_response"]
    if not isinstance(details, dict):
        raise ValueError("❌ 'details' doit être un dictionnaire (dict).")

    missing_keys = [key for key in required_keys if key not in details]
    if missing_keys:
        raise ValueError(
            f"❌ Erreur de Logging (Agent: {agent_name}) : "
            f"Les champs {missing_keys} sont manquants dans le dictionnaire 'details'. "
            f"Ils sont OBLIGATOIRES pour valider le TP."
        )
    # --- 2b. NORMALISATION: FIX outputs must be code-only (no ``` fences) ---
    if action_str == "FIX":
        details["output_response"] = _strip_markdown_code_fences(details["output_response"])

    # --- 3. PRÉPARATION DE L'ENTRÉE ---
    os.makedirs("logs", exist_ok=True)

    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent_name,
        "model": model_used,
        "action": action_str,
        "details": details,
        "status": status,
    }

    # --- 4. ÉCRITURE ---
    data = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
        except json.JSONDecodeError:
            print(
                f"⚠️ Attention : Le fichier de logs {LOG_FILE} était corrompu. "
                f"Une nouvelle liste a été créée."
            )
            data = []

    if not isinstance(data, list):
        # In case file content is valid JSON but not a list
        data = []

    data.append(entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
