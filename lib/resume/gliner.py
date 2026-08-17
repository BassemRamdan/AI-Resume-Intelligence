"""
GLiNER Entity Extraction Module.
Uses urchade/gliner_multi-v2.1 for zero-shot Named Entity Recognition.
Caches model globally to prevent reloading on repeated API requests.
"""

import warnings
warnings.filterwarnings("ignore")

_gliner_model = None

def get_gliner_model(device: str = "cpu"):
    """Singleton getter for cached GLiNER model."""
    global _gliner_model
    if _gliner_model is None:
        try:
            from gliner import GLiNER
            _gliner_model = GLiNER.from_pretrained("urchade/gliner_multi-v2.1").to(device)
        except Exception as e:
            print(f"Warning: GLiNER model loading failed: {e}")
            _gliner_model = None
    return _gliner_model

def extract_entities_from_chunk(text_chunk: str, labels: list, threshold: float = 0.35, device: str = "cpu") -> list:
    """Extract named entities from a specific text block with length chunking."""
    if not text_chunk or not text_chunk.strip():
        return []
    
    model = get_gliner_model(device)
    if model is None:
        return []
        
    max_chars = 1500
    chunks = [text_chunk[i:i+max_chars] for i in range(0, len(text_chunk), max_chars)]
    results = []
    
    for chunk in chunks:
        try:
            preds = model.predict_entities(chunk, labels, threshold=threshold)
            results.extend(preds)
        except Exception as e:
            print(f"Warning: Entity prediction error: {e}")
            
    return results
