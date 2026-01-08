import re

def optimize_prompt(prompt: str, max_length: int = 5000) -> str:
    """
    Optimizes a prompt for LLM Gemini to reduce hallucinations and token usage.
    
    Steps:
    1. Strip leading/trailing spaces
    2. Replace multiple spaces/tabs with a single space
    3. Remove multiple consecutive empty lines
    4. Truncate intelligently if exceeds max_length (avoid cutting words)
    
    Args:
        prompt (str): The raw prompt text.
        max_length (int): Maximum number of characters to keep (default 5000 for Gemini)
    
    Returns:
        str: Optimized prompt ready to send to the agent.
    """
    if not isinstance(prompt, str):
        raise TypeError("Prompt must be a string")
    
    # 1️⃣ Strip leading/trailing spaces
    prompt = prompt.strip()

    # 2️⃣ Replace multiple spaces or tabs with a single space
    prompt = re.sub(r"[ \t]+", " ", prompt)

    # 3️⃣ Replace multiple newlines with a single newline
    prompt = re.sub(r"\n\s*\n", "\n", prompt)

    # 4️⃣ Truncate intelligently if too long
    if len(prompt) > max_length:
        prompt = prompt[:max_length]
        # Avoid cutting words in half
        if " " in prompt:
            prompt = " ".join(prompt.split(" ")[:-1])

    return prompt
