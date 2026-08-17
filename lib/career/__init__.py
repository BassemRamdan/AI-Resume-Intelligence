"""
Career intelligence and deterministic fit engine package.
"""

from .taxonomy import CAREER_TAXONOMY
from .engine import calculate_career_fit, normalize_text

__all__ = [
    "CAREER_TAXONOMY",
    "calculate_career_fit",
    "normalize_text"
]
