"""
Model inference and embedding resources package.
"""

from .classifier import get_classifier_model, classify_text
from .embedder import get_embedder_model, get_embedding_resources, encode_text

__all__ = [
    "get_classifier_model",
    "classify_text",
    "get_embedder_model",
    "get_embedding_resources",
    "encode_text"
]
