"""
Prompt template loader module.
"""

import os

PROMPT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "prompts")

def get_prompt(prompt_name: str) -> str:
    """Reads prompt template text from prompts directory."""
    path = os.path.join(PROMPT_DIR, f"{prompt_name}.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""
