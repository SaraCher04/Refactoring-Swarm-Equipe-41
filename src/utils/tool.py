from pathlib import Path
import os

SANDBOX_PATH = Path("./sandbox").resolve()

# =========================================================
# def validate_sandbox_path(file_path: str) -> Path:
# =========================================================


def validate_sandbox_path(file_path: str) -> Path:
    """Vérifie que le fichier est dans ./sandbox."""
    full_path = Path(file_path).resolve()
    if not str(full_path).startswith(str(SANDBOX_PATH)):
        raise ValueError(f"❌ Hors sandbox: {file_path}")
    if not full_path.exists():
        raise FileNotFoundError(f"❌ Introuvable: {file_path}")
    return full_path


# =========================================================
# list_python_files(target_dir: str) -> list[str]:
# =========================================================


def list_python_files(target_dir: str) -> list[str]:
    """Liste tous les .py dans le dossier."""
    target_path = Path(target_dir)
    validate_sandbox_path(str(target_path))
    return [str(p) for p in target_path.rglob("*.py")]


# =========================================================
# read-file(file-path : str) -> str
# =========================================================

from pathlib import Path


def read_file(file_path: str) -> str:
    """
    Read a Python file from the sandbox securely.
    Returns the content as a string.
    """
    safe_path = validate_sandbox_path(file_path)
    if not safe_path.is_file():
        raise FileNotFoundError(f"File not found: '{safe_path}'")

    content = safe_path.read_text(encoding="utf-8")
    print(f"✅ Read file: '{safe_path}' ({len(content)} characters)")
    return content


# =========================================================
# write-file(file-path : str, content: str, mode: str = "w") -> None:
# =========================================================


def write_file(file_path: str, content: str, mode: str = "w") -> None:
    """
    Write a Python file in the sandbox securely.
    Crée dossiers + fichiers tests auto!
    """
    if mode not in ("w", "a"):
        raise ValueError("Mode must be 'w' or 'a'")

    # Valide SEULEMENT sandbox racine
    sandbox_root = validate_sandbox_path(os.path.dirname(file_path) or ".")

    safe_path = Path(file_path).resolve()
    safe_path.parent.mkdir(parents=True, exist_ok=True)  # ✅ Crée dossiers!

    with safe_path.open(mode, encoding="utf-8") as f:
        f.write(content)

    action = "Appended" if mode == "a" else "Wrote"
    print(f"✅ {action} file: '{safe_path}' ({len(content)} chars)")
