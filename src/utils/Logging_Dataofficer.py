# =========================================================
# Logging / Data Officer
# =========================================================

import os
import json
from utils.logger import log_experiment, ActionType
from typing import Dict, Any


# ---------------------------------------------------------
# Initialisation du journal
# ---------------------------------------------------------
import os
import json


def init_experiment_log() -> dict:
    """
    ✅ CORRIGÉ: Crée le fichier experiment_data.json avec une LISTE vide.
    """
    os.makedirs("logs", exist_ok=True)
    log_file = "logs/experiment_data.json"

    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("[]")  #  LISTE vide

    return {"status": "initialized"}


# ---------------------------------------------------------
# Logger une action d'agent
# ---------------------------------------------------------
def log_agent_action(
    agent: str,
    action: ActionType,
    details: Dict[str, Any],
    input_prompt: str,
    output_response: str,
    model_used: str = "gemini-1.5-flash",  # ✅ Valeur par défaut réaliste
    status: str = "SUCCESS",
) -> None:
    """
    Enregistre l'action d'un agent dans experiment_data.json via log_experiment.

    Paramètres :
        agent           : nom de l'agent (ex: "Auditor")
        action          : type d'action (ActionType.ANALYSIS, ActionType.FIX, etc.)
        details         : dictionnaire supplémentaire d'informations (ex: file_analyzed)
        input_prompt    : texte exact envoyé au LLM (OBLIGATOIRE)
        output_response : réponse brute reçue du LLM (OBLIGATOIRE)
        model_used      : modèle LLM utilisé (ex: "gemini-1.5-flash")
        status          : "SUCCESS" ou "FAILURE"  # ✅ Correction orthographe

    ⚠️ input_prompt et output_response doivent toujours être fournis.
    """
    if not input_prompt:
        raise ValueError(
            "input_prompt cannot be empty! Provide the real prompt sent to the LLM."
        )
    if not output_response:
        raise ValueError(
            "output_response cannot be empty! Provide the real response received from the LLM."
        )

    # Ajout des champs obligatoires dans details
    details = details.copy()  # pour ne pas modifier l'original
    details["input_prompt"] = input_prompt
    details["output_response"] = output_response

    # Appel du logger du TP
    log_experiment(
        agent_name=agent,
        model_used=model_used,  # ✅ Paramètre passé correctement
        action=action,
        details=details,
        status=status,
    )


# ---------------------------------------------------------
# Finaliser l'expérience
# ---------------------------------------------------------
def finalize_experiment(status: str = "SUCCESS") -> None:
    """
    Marque la fin de l'expérience.
    Ajoute un log System pour indiquer la fin.
    """
    # ✅ Utilisation d'un ActionType valide avec des champs obligatoires
    log_experiment(
        agent_name="System",
        model_used="system",
        action=ActionType.ANALYSIS,  # ✅ Changé de END à un type valide
        details={
            "input_prompt": "Experiment finalization",
            "output_response": f"Experiment ended with status: {status}",
            "experiment_status": status,
        },
        status=status,
    )
