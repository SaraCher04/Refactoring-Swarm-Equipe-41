# =========================================================
# read-file(file-path : str) -> str
# =========================================================

from pathlib import Path
from src.validate_sandbox_path.py import validate_sandbox_path.py

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
