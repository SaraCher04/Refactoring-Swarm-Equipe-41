# =========================================================
# run_pytest.py
# =========================================================

import sys
import subprocess
from src.validate_sandbox_path import validate_sandbox_path
from src.list_python_files import list_python_files


def run_pytest(tests_dir: str) -> dict:
    """
    Lance pytest sur le dossier de tests et retourne un dictionnaire :
    {
        "success": True/False,
        "logs": "stdout + stderr"
    }

    """
    result = {"success": False, "logs": ""}

    try:
        # Valider le chemin sandbox
        safe_dir = validate_sandbox_path(tests_dir)

        # Vérifier qu'il existe et que c'est un dossier
        if not safe_dir.exists():
            raise FileNotFoundError(f"Tests folder not found: {safe_dir}")
        if not safe_dir.is_dir():
            raise NotADirectoryError(f"Not a directory: {safe_dir}")

        # Lister tous les fichiers Python pour pytest
        py_files = list_python_files(str(safe_dir))
        if not py_files:
            result["logs"] = f"⚠️ Aucun fichier Python à tester dans {safe_dir}"
            result["success"] = False
            return result

        # Lancer pytest via subprocess en utilisant le Python actuel (venv)
        process = subprocess.run(
            [sys.executable, "-m", "pytest", str(safe_dir), "-q", "--tb=short"],
            capture_output=True,
            text=True,
        )

        # Remplir le résultat
        logs = process.stdout + "\n" + process.stderr
        result["logs"] = logs.strip()
        result["success"] = process.returncode == 0

    except Exception as e:
        result["logs"] = str(e)
        result["success"] = False

    return result

