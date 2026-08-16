import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

_tokenizer = None
_classifier = None

def get_model(device):
    global _tokenizer, _classifier
    if _tokenizer is None or _classifier is None:
        model_name = "BassemRamdan/resume-classifier-deberta"
        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _classifier = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
    return _tokenizer, _classifier

def classify_text(text):
    """
    Classifies the resume text using DeBERTa fine-tuned model.
    """
    predicted_category = "INFORMATION-TECHNOLOGY" # default fallback
    confidence = 0.0
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    try:
        tokenizer, classifier = get_model(device)
        
        inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = classifier(**inputs)
            logits = outputs.logits
            probs = torch.nn.functional.softmax(logits, dim=-1)
            confidence = torch.max(probs).item()
            predicted_idx = torch.argmax(logits, dim=-1).item()
            
        predicted_category = classifier.config.id2label.get(predicted_idx, "UNKNOWN_CATEGORY")
        confidence = round(confidence, 4)
    except Exception as e:
        print(f"Classification Error: {e}")
        pass
        
    return predicted_category, confidence
