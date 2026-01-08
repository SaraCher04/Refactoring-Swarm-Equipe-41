from pathlib import Path

# Prompts directory
PROMPT_DIR = Path("prompts").resolve()
PROMPT_DIR.mkdir(exist_ok=True)


def save_prompt(name: str, content: str, overwrite: bool = False) -> None:
    """
    Saves a prompt only in the prompts directory as a .txt file.

    - name: prompt name (e.g., auditor_v1)
    - content: prompt text
    - overwrite: True to overwrite an existing prompt
    """

    # Build prompt file path
    path = PROMPT_DIR / f"{name}.txt"

    if path.exists() and not overwrite:
        raise FileExistsError(
            f"The prompt '{name}' already exists. Use overwrite=True to replace it."
        )

    # Write prompt to file
    path.write_text(content, encoding="utf-8")
