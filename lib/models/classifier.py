"""
Resume Sequence Classification Module.
Loads fine-tuned transformer model for 24-category resume classification.
Caches model globally to prevent reloading on every inference call.
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

_model = None
_tokenizer = None

def get_classifier_model(device: str = "cpu"):
    """Singleton getter for the fine-tuned sequence classifier."""
    global _model, _tokenizer
    if _model is None or _tokenizer is None:
        possible_paths = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "models", "distilbert-resume-classifier"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "notebooks", "final_resume_classifier"),
            os.path.join("models", "distilbert-resume-classifier"),
            "BassemRamdan/resume-classifier-deberta"
        ]
        
        loaded = False
        for path in possible_paths:
            if os.path.exists(path) or path.startswith("BassemRamdan/"):
                try:
                    _tokenizer = AutoTokenizer.from_pretrained(path)
                    _model = AutoModelForSequenceClassification.from_pretrained(path)
                    _model.to(device)
                    _model.eval()
                    loaded = True
                    break
                except Exception as e:
                    print(f"Failed to load model from {path}: {e}")
                    
        if not loaded:
            print("Warning: Sequence classifier model could not be loaded.")
            return None, None
            
    return _model, _tokenizer

def classify_text(text: str, device: str = "cpu") -> dict:
    """
    Classifies raw resume text into one of 24 canonical career categories.
    Returns: {"dataset_category": str, "confidence": float}
    """
    if not text or not text.strip():
        return {"dataset_category": "UNKNOWN", "confidence": 0.0}
        
    model, tokenizer = get_classifier_model(device)
    if model is None or tokenizer is None:
        return {"dataset_category": "UNKNOWN", "confidence": 0.0}
        
    try:
        inputs = tokenizer(
            text,
            truncation=True,
            max_length=512,
            padding=True,
            return_tensors="pt"
        ).to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            confidence, predicted_idx = torch.max(probs, dim=1)
            
        category = model.config.id2label[predicted_idx.item()]
        return {
            "dataset_category": category,
            "confidence": round(float(confidence.item()), 4)
        }
    except Exception as e:
        print(f"Error during sequence classification: {e}")
        return {"dataset_category": "UNKNOWN", "confidence": 0.0}
