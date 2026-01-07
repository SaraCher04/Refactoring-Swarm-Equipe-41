# =========================================================
# save-audit-plan(plan: str) -> None
# =========================================================


from pathlib import Path
from src.write_file.py import write_file
from src.validate_sandbox_path.py import validate_sandbox_path

def save_audit_plan(plan: str) -> None:
    """
    Save the refactoring plan into 'sandbox/refactoring_plan/audit_plan.txt'.
    """
    # Chemin complet sécurisé vers audit_plan.txt
    safe_path = validate_sandbox_path("refactoring_plan/audit_plan.txt")

    # Crée le fichier ou écrase l'ancien
    write_file(safe_path, plan, mode="w")

    print(f"✅ Audit plan saved at '{safe_path}' ({len(plan)} characters)")

