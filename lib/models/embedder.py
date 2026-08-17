"""
Dense Semantic Embedding Module.
Uses sentence-transformers/all-MiniLM-L6-v2 (384 dimensions).
Caches model and embedding resources globally in memory.
"""

import os
import json
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

_embedder = None
_cv_embeddings = None
_cv_metadata = None
_prototypes = None

def get_embedder_model(device: str = "cpu"):
    """Singleton getter for SentenceTransformer embedder."""
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=device)
    return _embedder

def get_embedding_resources(data_dir: str = None):
    """
    Loads pre-computed dense embeddings, metadata, and prototypes.
    """
    global _cv_embeddings, _cv_metadata, _prototypes
    
    if _cv_embeddings is None or _cv_metadata is None or _prototypes is None:
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
            
        emb_path = os.path.join(data_dir, "embeddings.npy")
        if not os.path.exists(emb_path):
            emb_path = os.path.join(data_dir, "cv_embeddings.npy")
            
        meta_path = os.path.join(data_dir, "cv_metadata.json")
        proto_path = os.path.join(data_dir, "prototypes.json")
        
        if os.path.exists(emb_path) and os.path.exists(meta_path) and os.path.exists(proto_path):
            _cv_embeddings = np.load(emb_path)
            with open(meta_path, "r", encoding="utf-8") as f:
                _cv_metadata = json.load(f)
            with open(proto_path, "r", encoding="utf-8") as f:
                _prototypes = json.load(f)
        else:
            print("Warning: Pre-computed embedding resources not found in data directory.")
            
    return _cv_embeddings, _cv_metadata, _prototypes

def encode_text(text: str, device: str = "cpu") -> np.ndarray:
    """Encodes input string into a 384-dimensional dense semantic vector."""
    if not text:
        return np.zeros(384, dtype=np.float32)
    embedder = get_embedder_model(device)
    return embedder.encode(text, convert_to_tensor=False)
