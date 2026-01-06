# =========================================================
# validate_sandbox_path(path: str) -> Path
# =========================================================
from pathlib import Path

SANDBOX_DIR = Path("sandbox").resolve()

def validate_sandbox_path(path: str) -> Path:
    candidate_path = Path(path)
    if not candidate_path.is_absolute():
        candidate_path = SANDBOX_DIR / candidate_path
    resolved_path = candidate_path.resolve()
    if SANDBOX_DIR not in resolved_path.parents and resolved_path != SANDBOX_DIR:
        print(f"⛔ Access denied: '{resolved_path}' is outside the sandbox")
        raise PermissionError(f"Access denied: '{resolved_path}' is outside the sandbox")
    print(f"✅ Validated path: '{resolved_path}'")
    return resolved_path
