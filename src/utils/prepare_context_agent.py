
import re
from pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum
from src.create_system_prompt import create_system_prompt
from src.load_prompt import load_prompt
from src.optimize_prompt import optimize_prompt 
from src.hash_prompt import hash_prompt 

class AgentType(str, Enum):
    """Types d'agents disponibles"""

    AUDITOR = "auditor"
    FIXER = "fixer"
    JUDGE = "judge"


def prepare_context_agent(
    agent_type: AgentType,
    code_content: str,
    additional_context: Optional[Dict[str, Any]] = None,
    max_context_length: int = 4000,
) -> Dict[str, str]:
    """
     FONCTION PRINCIPALE - Prépare le contexte complet pour un agent.

    Cette fonction:
    1. Charge ou génère le system prompt approprié
    2. Combine le code à analyser avec le contexte additionnel
    3. Optimise pour éviter la surcharge mémoire
    4. NE LOG PAS (c'est l'agent qui logge après avoir reçu la réponse LLM)

    Args:
        agent_type: Type d'agent (AUDITOR, FIXER, JUDGE)
        code_content: Code Python à traiter
        additional_context: Contexte supplémentaire (ex: plan de refactoring, erreurs)
        max_context_length: Longueur max du contexte utilisateur

    Returns:
        Dict avec 'system_prompt' et 'user_prompt' et 'prompt_hash'prêts à envoyer au LLM

    """
    if not code_content or not code_content.strip():
        raise ValueError("Le code_content ne peut pas être vide")

    # 1 Récupérer le system prompt
    try:
        # Essayer de charger un prompt personnalisé
        prompt_name = f"{agent_type.value}_system"
        system_prompt = load_prompt(prompt_name)
        print(f" Utilisation du prompt personnalisé: {prompt_name}")
    except FileNotFoundError:
        # Utiliser le prompt par défaut
        system_prompt = create_system_prompt(agent_type)
        print(f" Utilisation du prompt système par défaut pour {agent_type.value}")

    # 2 Construire le contexte utilisateur
    user_parts = [f"# CODE À ANALYSER:\n```python\n{code_content}\n```"]

    # Ajouter le contexte additionnel si fourni
    if additional_context:
        context_str = "\n# INFORMATIONS SUPPLÉMENTAIRES:\n"
        for key, value in additional_context.items():
            context_str += f"- {key}: {value}\n"
        user_parts.append(context_str)

    # 3 Combiner et optimiser
    user_prompt = "\n\n".join(user_parts)
    user_prompt = optimize_prompt(user_prompt, max_length=max_context_length)

    # 4 Retourner le contexte complet
    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "prompt_hash": hash_prompt(system_prompt),
    }


# ====================================================================================
