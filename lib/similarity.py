"""
Similarity and career fit compatibility wrapper.
Re-exports from lib.career.engine.
"""

from .career.engine import calculate_career_fit as calculate_similarity

__all__ = ["calculate_similarity"]
