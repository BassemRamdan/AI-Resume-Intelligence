"""
LLM integration and explanation package.
"""

from .prompts import get_prompt
from .groq import explain_career_fit

__all__ = [
    "get_prompt",
    "explain_career_fit"
]
