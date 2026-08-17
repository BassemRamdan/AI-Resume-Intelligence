import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

_model = None
_tokenizer = None

def get_model(device):
    global _model, _tokenizer
    
    if _model is None:
        try:
            # Look for the model in models/distilbert-resume-classifier
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'distilbert-resume-classifier')
            if not os.path.exists(model_path):
                print(f"Warning: Model not found at {model_path}. Please train the model first.")
                return None, None
                
            _tokenizer = AutoTokenizer.from_pretrained(model_path)
            _model = AutoModelForSequenceClassification.from_pretrained(model_path)
            _model.to(device)
            _model.eval()
        except Exception as e:
            print(f"Error loading fine-tuned model: {e}")
            return None, None
            
    return _model, _tokenizer

def classify_text(text):
    """
    Classifies the resume text using the fine-tuned DistilBERT model.
    Falls back to similarity engine if the model fails to load or error occurs.
    """
    # Force CPU for inference in the API to prevent cross-thread CUDA errors
    device = torch.device('cpu')
    model, tokenizer = get_model(device)
    
    if model is None or tokenizer is None:
        print("Falling back to semantic similarity for classification...")
        try:
            import sys
            sys.path.append(os.path.dirname(__file__))
            from similarity import get_career_similarity
            sims = get_career_similarity(text)
            if sims and len(sims) > 0:
                return sims[0]['category'], sims[0]['normalized_similarity'] / 100.0
        except:
            pass
        return "INFORMATION-TECHNOLOGY", 0.0

    try:
        # Move model to CPU explicitly just in case it was loaded elsewhere
        model = model.to(device)
        
        inputs = tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512, 
            padding=True
        ).to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=1)
        confidence, predicted_class = torch.max(probabilities, dim=1)
        
        # Get label from config
        predicted_category = model.config.id2label[predicted_class.item()]
        
        return predicted_category, confidence.item()
    except Exception as e:
        print(f"Classification error: {e}")
        return "INFORMATION-TECHNOLOGY", 0.0
