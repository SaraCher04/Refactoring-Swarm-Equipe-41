def hash_prompt(content: str) -> str:
    """Returns a SHA256 hash of the prompt for anti-plagiarism"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()
