import json
import hashlib
from datetime import datetime
from pathlib import Path
from src.hash_prompt.py import hash_prompt 


# Prompts directory
PROMPT_DIR = Path("prompts").resolve()
PROMPT_DIR.mkdir(exist_ok=True)

# experiment_data.json file
EXPERIMENT_FILE = Path("logs/experiment_data.json").resolve()
EXPERIMENT_FILE.parent.mkdir(exist_ok=True)
def save_promot(name: str, content: str, overwrite: bool = False) -> None:
    """
    Saves a prompt to promots/name.txt AND logs it in experiment_data.json
    - name: prompt name (e.g., auditor_v1)
    - content: prompt text
    - overwrite: True to overwrite an existing promot
    """
    # 1️⃣ Build the path for the .txt file
    path = PROMPT_DIR / f"{name}.txt"
    
    if path.exists() and not overwrite:
        raise FileExistsError(f"The prompt '{name}' already exists. Use overwrite=True to replace it.")
    
    # 2️⃣ Write the prompt to the .txt file
    path.write_text(content, encoding="utf-8")
    print(f"✅ Prompt saved: {path}")

    # 3️⃣ Generate the hash of the prompt
    prompt_hash = hash_prompt(content)

    # 4️⃣ Load the experiment_data.json
    data = {}
    if EXPERIMENT_FILE.exists():
        with open(EXPERIMENT_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                # 🔹 If data is a list (from previous incorrect JSON), convert to dict
                if isinstance(data, list):
                    data = {f"prompt_{i}": v for i, v in enumerate(data)}
            except json.JSONDecodeError:
                data = {}

    # 5️⃣ Add/update the prompt entry in the JSON
    data[name] = {
        "content": content,
        "hash": prompt_hash,
        "txt_path": str(path),
        "timestamp": datetime.now().isoformat()
    }

    # 6️⃣ Save back to experiment_data.json
    with open(EXPERIMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"📊 Prompt also logged in experiment_data.json")
