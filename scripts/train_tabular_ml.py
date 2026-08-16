import json
import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def main():
    print("Loading data...")
    meta_path = os.path.join("data", "cv_metadata.json")
    
    with open(meta_path, 'r') as f:
        data = json.load(f)
        
    df = pd.DataFrame(data)
    
    # Feature Engineering (Tabular format)
    # Combine skills and experience into one text feature for TF-IDF
    def join_if_list(x):
        if isinstance(x, list):
            return " ".join([str(i) for i in x])
        return str(x)
        
    df['skills_str'] = df['skills_preview'].apply(join_if_list)
    df['exp_str'] = df['experience_preview'].apply(join_if_list)
    df['text_features'] = df['skills_str'] + " " + df['exp_str']
    
    # Target
    y = df['category']
    X = df['text_features']
    
    print(f"Dataset loaded. Total rows: {len(df)}")
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Pipeline: TF-IDF -> Random Forest
    print("Training Tabular ML Pipeline (TF-IDF + Random Forest)...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1))
    ])
    
    pipeline.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Save the pipeline
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "tabular_rf_pipeline.pkl")
    
    joblib.dump(pipeline, model_path)
    print(f"Model saved successfully to {model_path}")

if __name__ == "__main__":
    main()
