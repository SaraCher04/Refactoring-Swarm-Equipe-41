# ------------------------------------------------------------------
#                        Load prompt
# ------------------------------------------------------------------

from pathlib import Path

# Prompts directory
PROMPT_DIR = Path("prompts").resolve()
PROMPT_DIR.mkdir(exist_ok=True)

# experiment_data.json file
EXPERIMENT_FILE = Path("logs/experiment_data.json").resolve()
EXPERIMENT_FILE.parent.mkdir(exist_ok=True)


def load_prompt(name: str) -> str:
    """
    Loads a prompt from prompts/name.txt
    - name: prompt name without extension (e.g., auditor_v1)
    Returns the prompt content as a string
    """

    # 1 Build the path safely (sandbox respected)
    path = PROMPT_DIR / f"{name}.txt"

    # 2 Check existence
    if not path.exists():
        raise FileNotFoundError(
            f"Prompt '{name}' not found in prompts/. "
            f"Make sure it was saved using save_prompt()."
        )

    # 3 Read and return content
    content = path.read_text(encoding="utf-8")

    # 4 Extra safety: avoid empty prompts
    if not content.strip():
        raise ValueError(f"Prompt '{name}' is empty.")

    return content
