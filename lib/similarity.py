import sys
import json
import torch
import os
import numpy as np
from sentence_transformers import SentenceTransformer, util

def calculate_similarity(profile_data):
    if isinstance(profile_data, str):
        with open(profile_data, 'r') as f:
            profile = json.load(f)
    else:
        profile = profile_data
        
    raw_text = profile.get("raw_text_snippet", "")
    proto_path = os.path.join("data", "prototypes.json")
    emb_path = os.path.join("data", "cv_embeddings.npy")
    meta_path = os.path.join("data", "cv_metadata.json")
    
    if not os.path.exists(proto_path) or not os.path.exists(emb_path):
        return {
            "classification": {
                "category": profile.get("career_signal", {}).get("dataset_category", "UNKNOWN"),
                "confidence": profile.get("career_signal", {}).get("confidence", 0.0)
            },
            "similarity": [
                {"category": profile.get("career_signal", {}).get("dataset_category", "UNKNOWN"), "score": 90.0}
            ],
            "similar_cvs": [],
            "analysis": "Data not found. Run build_prototypes.py."
        }
        
    with open(proto_path, 'r') as f:
        prototypes = json.load(f)
        
    cv_embs = np.load(emb_path)
    with open(meta_path, 'r') as f:
        cv_meta = json.load(f)
        
    embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    emb = embedder.encode(raw_text, convert_to_tensor=True)
    
    # 1. Category Similarity (Prototypes)
    cat_results = []
    for cat, proto_vec in prototypes.items():
        proto_tensor = torch.tensor(proto_vec)
        score = util.cos_sim(emb, proto_tensor)[0][0].item()
        cat_results.append({"category": cat, "similarity": score})
        
    max_s = max(r['similarity'] for r in cat_results)
    min_s = min(r['similarity'] for r in cat_results)
    for r in cat_results:
        r['score'] = round(((r['similarity'] - min_s) / (max_s - min_s + 1e-9)) * 100, 1)
    cat_results = sorted(cat_results, key=lambda x: x['score'], reverse=True)
    
    # 2. KNN Similar CVs
    cv_embs_tensor = torch.tensor(cv_embs)
    cos_scores = util.cos_sim(emb, cv_embs_tensor)[0]
    top_results = torch.topk(cos_scores, k=3)
    
    similar_cvs = []
    for score, idx in zip(top_results[0], top_results[1]):
        match_meta = cv_meta[idx.item()]
        # Scale score to 0-100 loosely for UI
        s_val = score.item()
        mapped_score = round(max(0, min(100, s_val * 100)), 1)
        similar_cvs.append({
            "id": match_meta["id"],
            "category": match_meta["category"],
            "skills": match_meta["skills_preview"],
            "experience": match_meta["experience_preview"],
            "score": mapped_score
        })
    
    output = {
        "classification": {
            "category": profile.get("career_signal", {}).get("dataset_category", "UNKNOWN"),
            "confidence": profile.get("career_signal", {}).get("confidence", 0.0)
        },
        "similarity": cat_results[:5],
        "similar_cvs": similar_cvs,
        "profile_skills": [s.get("name") for s in profile.get("skills", [])],
        "profile_projects": [p.get("title", p.get("name", "Unknown")) for p in profile.get("projects", [])]
    }
    
    return output

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    output = calculate_similarity(sys.argv[1])
    print("===START===")
    print(json.dumps(output))
    print("===END===")
