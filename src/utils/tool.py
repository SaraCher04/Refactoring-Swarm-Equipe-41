from pathlib import Path

SANDBOX_PATH = Path("./sandbox").resolve()


def validate_sandbox_path(file_path: str) -> Path:
    """Vérifie que le fichier est dans ./sandbox."""
    full_path = Path(file_path).resolve()
    if not str(full_path).startswith(str(SANDBOX_PATH)):
        raise ValueError(f"❌ Hors sandbox: {file_path}")
    if not full_path.exists():
        raise FileNotFoundError(f"❌ Introuvable: {file_path}")
    return full_path


def list_python_files(target_dir: str) -> list[str]:
    """Liste tous les .py dans le dossier."""
    target_path = Path(target_dir)
    validate_sandbox_path(str(target_path))
    return [str(p) for p in target_path.rglob("*.py")]
