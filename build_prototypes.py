import os
import json
import numpy as np
from datasets import load_dataset
from sentence_transformers import SentenceTransformer

def build_dataset_index():
    print("Loading dataset...")
    dataset = load_dataset("Youssef-mohamed123/resume_entities", split="train")
    df = dataset.to_pandas()
    
    # Text creation for semantic embedding
    def create_text(row):
        return " ".join(list(row['skills']) + list(row['experience']) + list(row['education']))
    df['cleaned_resume'] = df.apply(create_text, axis=1)
    
    embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    categories = df['category'].unique()
    prototypes = {}
    
    print("Computing category centroids...")
    for cat in categories:
        cat_resumes = df[df['category'] == cat]['cleaned_resume'].tolist()
        embs = embedder.encode(cat_resumes, convert_to_numpy=True)
        centroid = np.mean(embs, axis=0)
        prototypes[cat] = centroid.tolist()
        
    os.makedirs('data', exist_ok=True)
    with open('data/prototypes.json', 'w') as f:
        json.dump(prototypes, f)
    print("Saved prototypes to data/prototypes.json")
    
    print("Computing individual CV embeddings for KNN Similarity...")
    # Limit to 500 for speed if needed, but 2484 is fast for MiniLM
    # We will compute embeddings for all CVs to find "Similar CVs"
    all_texts = df['cleaned_resume'].tolist()
    all_embs = embedder.encode(all_texts, convert_to_numpy=True)
    
    # Save the embeddings array
    np.save('data/cv_embeddings.npy', all_embs)
    
    # Save the metadata for retrieval
    metadata = []
    for idx, row in df.iterrows():
        metadata.append({
            "id": int(idx),
            "category": str(row['category']),
            "skills_preview": list(row['skills'])[:5],
            "experience_preview": list(row['experience'])[:3]
        })
        
    with open('data/cv_metadata.json', 'w') as f:
        json.dump(metadata, f)
        
    print(f"Saved {len(metadata)} CV embeddings for Similarity Engine.")

if __name__ == "__main__":
    build_dataset_index()
