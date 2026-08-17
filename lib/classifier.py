"""
Sequence classifier compatibility wrapper.
Re-exports from lib.models.classifier.
"""

from .models.classifier import get_classifier_model, classify_text

__all__ = ["get_classifier_model", "classify_text"]
