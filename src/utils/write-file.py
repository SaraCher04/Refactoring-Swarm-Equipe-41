# =========================================================
# write-file(file-path : str, content: str, mode: str = "w") -> None:
# =========================================================
from src.validate_sandbox_path.py import validate_sandbox_path

def write_file(file_path: str, content: str, mode: str = "w") -> None:
    """
    Write a Python file in the sandbox securely.
    mode: "w" to overwrite, "a" to append.
    """
    if mode not in ("w", "a"):
        raise ValueError("Mode must be 'w' (overwrite) or 'a' (append)")

    safe_path = validate_sandbox_path(file_path)
    safe_path.parent.mkdir(parents=True, exist_ok=True)

    with safe_path.open(mode, encoding="utf-8") as f:
        f.write(content)

    action = "Appended to" if mode == "a" else "Wrote"
    print(f"✅ {action} file: '{safe_path}' ({len(content)} characters)")
