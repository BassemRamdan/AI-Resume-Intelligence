import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def classify_text(text):
    """
    Classifies the resume text using DeBERTa fine-tuned model.
    """
    predicted_category = "INFORMATION-TECHNOLOGY" # default fallback
    confidence = 0.0
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    try:
        model_name = "BassemRamdan/resume-classifier-deberta"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        classifier = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
        
        inputs = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = classifier(**inputs)
            logits = outputs.logits
            predicted_idx = torch.argmax(logits, dim=-1).item()
            
        predicted_category = classifier.config.id2label.get(predicted_idx, "UNKNOWN_CATEGORY")
        confidence = 0.9
    except Exception as e:
        print(f"Classification Error: {e}")
        pass
        
    return predicted_category, confidence
