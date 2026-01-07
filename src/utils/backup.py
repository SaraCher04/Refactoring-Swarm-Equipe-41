# =========================================================
#  backup_file(file_path: str) -> None:
# =========================================================

from pathlib import Path
from shutil import copy2
from src.validate_sandbox_path.py import validate_sandbox_path

SANDBOX_DIR = Path("sandbox").resolve()


def backup_file(file_path: str) -> None:
    """
    Crée une sauvegarde incrémentale du fichier avant modification.
    Le fichier de sauvegarde sera nommé : original_backup1.py, original_backup2.py, etc.
    et sera stocké dans le dossier 'backups' du répertoire sandbox.
    """
    safe_path = validate_sandbox_path(file_path)

    # Créer le dossier backups s'il n'existe pas
    backups_dir = SANDBOX_DIR / "backups"
    backups_dir.mkdir(exist_ok=True)

    # Trouver le prochain numéro de backup disponible
    base_name = safe_path.stem  # nom sans extension
    extension = safe_path.suffix  # .py

    backup_number = 1
    while True:
        backup_name = f"{base_name}_backup{backup_number}{extension}"
        backup_path = backups_dir / backup_name

        if not backup_path.exists():
            break
        backup_number += 1

    # Copier le fichier original
    copy2(safe_path, backup_path)

    print(f"✅ Backup created: '{backup_path}' (backup #{backup_number})")
    return str(backup_path)
