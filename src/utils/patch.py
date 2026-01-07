# =========================================================
# apply_patch(file_path: str, new_code: str) -> None:
# =========================================================
from src.validate_sandbox_path.py import validate_sandbox_path


def apply_patch(file_path: str, new_code: str) -> None:
    """
    Replace the content of a file inside the sandbox with corrected code.
    """
    safe_path = validate_sandbox_path(file_path)

    if not safe_path.exists():
        raise FileNotFoundError(f"File not found: {safe_path}")

    if not safe_path.is_file():
        raise IsADirectoryError(f"Not a file: {safe_path}")

    with open(safe_path, "w", encoding="utf-8") as f:
        f.write(new_code)

    print(f"✅ Patch applied successfully to '{safe_path}'")
