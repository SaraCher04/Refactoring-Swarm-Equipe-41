# =========================================================
# list_python_files(target_dir: str) -> list[str]
# =========================================================
from pathlib import Path
from src.validate_sandbox_path.py import validate_sandbox_path  # réutilise la fonction sécurité

def list_python_files(target_dir: str) -> list[str]:
    """
    List all .py files in the target directory and subdirectories.
    Returns a list of absolute paths as strings.
    """
    safe_dir = validate_sandbox_path(target_dir)
    py_files = [str(p.resolve()) for p in safe_dir.rglob("*.py") if p.is_file()]
    print(f"✅ Found {len(py_files)} Python files in '{safe_dir}'")
    return py_files
