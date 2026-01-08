
rom pathlib import Path
from typing import Dict, Any, Optional
from enum import Enum
import re


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
    ✅ FONCTION PRINCIPALE - Prépare le contexte complet pour un agent.

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
        Dict avec 'system_prompt' et 'user_prompt' prêts à envoyer au LLM

    Example:
        >>> context = prepare_context_agent(
        ...     agent_type=AgentType.AUDITOR,
        ...     code_content=buggy_code,
        ...     additional_context={"file_path": "messy_code.py"}
        ... )
        >>> # Dans votre agent:
        >>> response = llm.generate(
        ...     system=context['system_prompt'],
        ...     user=context['user_prompt']
        ... )
        >>> # Puis logger avec log_agent_action()
    """
    if not code_content or not code_content.strip():
        raise ValueError("Le code_content ne peut pas être vide")

    # 1️⃣ Récupérer le system prompt
    try:
        # Essayer de charger un prompt personnalisé
        prompt_name = f"{agent_type.value}_system"
        system_prompt = load_prompt(prompt_name)
        print(f"📄 Utilisation du prompt personnalisé: {prompt_name}")
    except FileNotFoundError:
        # Utiliser le prompt par défaut
        system_prompt = create_system_prompt(agent_type)
        print(f"📄 Utilisation du prompt système par défaut pour {agent_type.value}")

    # 2️⃣ Construire le contexte utilisateur
    user_parts = [f"# CODE À ANALYSER:\n```python\n{code_content}\n```"]

    # Ajouter le contexte additionnel si fourni
    if additional_context:
        context_str = "\n# INFORMATIONS SUPPLÉMENTAIRES:\n"
        for key, value in additional_context.items():
            context_str += f"- {key}: {value}\n"
        user_parts.append(context_str)

    # 3️⃣ Combiner et optimiser
    user_prompt = "\n\n".join(user_parts)
    user_prompt = optimize_prompt(user_prompt, max_length=max_context_length)

    # 4️⃣ Retourner le contexte complet
    return {"system_prompt": system_prompt, "user_prompt": user_prompt}


# ====================================================================================
