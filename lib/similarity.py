import sys
import json
import torch
import os
import numpy as np
from sentence_transformers import SentenceTransformer, util
from career_taxonomy import CAREER_TAXONOMY

_embedder = None
_prototypes = None
_cv_embs = None
_cv_meta = None

def get_resources():
    global _embedder, _prototypes, _cv_embs, _cv_meta
    
    proto_path = os.path.join("data", "prototypes.json")
    emb_path = os.path.join("data", "cv_embeddings.npy")
    meta_path = os.path.join("data", "cv_metadata.json")
    
    if not os.path.exists(proto_path) or not os.path.exists(emb_path):
        return None, None, None, None
        
    if _embedder is None:
        _embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        with open(proto_path, 'r') as f:
            _prototypes = json.load(f)
        _cv_embs = np.load(emb_path)
        with open(meta_path, 'r') as f:
            _cv_meta = json.load(f)
            
    return _embedder, _prototypes, _cv_embs, _cv_meta

def normalize_text(text):
    return text.lower().strip() if text else ""

def calculate_similarity(profile_data):
    if isinstance(profile_data, str):
        with open(profile_data, 'r') as f:
            profile = json.load(f)
    else:
        profile = profile_data
        
    raw_text = profile.get("raw_text_snippet", "")
    
    embedder, prototypes, cv_embs, cv_meta = get_resources()
    
    primary_category = profile.get("career_signal", {}).get("dataset_category", "UNKNOWN")
    primary_confidence = profile.get("career_signal", {}).get("confidence", 0.0)
    
    if embedder is None:
        return {
            "classification": {
                "category": primary_category,
                "confidence": primary_confidence
            },
            "career_fit": [],
            "similar_cvs": [],
            "error": "Dataset or models not found."
        }
        
    emb = embedder.encode(raw_text, convert_to_tensor=True)
    
    # 1. KNN Similar CVs (Semantic Similarity ONLY)
    cv_embs_tensor = torch.tensor(cv_embs)
    cos_scores = util.cos_sim(emb, cv_embs_tensor)[0]
    top_results = torch.topk(cos_scores, k=3)
    
    similar_cvs = []
    for score, idx in zip(top_results[0], top_results[1]):
        match_meta = cv_meta[idx.item()]
        s_val = score.item()
        mapped_score = round(max(0, min(100, s_val * 100)), 1)
        similar_cvs.append({
            "id": match_meta["id"],
            "category": match_meta["category"],
            "skills": match_meta["skills_preview"],
            "experience": match_meta["experience_preview"],
            "score": mapped_score
        })

    # Pre-process profile data for the Career Fit engine
    prof_skills = [normalize_text(s.get("name", "")) for s in profile.get("skills", [])]
    prof_projects = []
    for p in profile.get("projects", []):
        text = normalize_text(p.get("title", "")) + " " + normalize_text(p.get("description", ""))
        techs = [normalize_text(t) for t in p.get("technologies", [])]
        prof_projects.append({"text": text, "techs": techs})
        
    prof_edu = " ".join([normalize_text(e.get("degree", "")) + " " + normalize_text(e.get("field", "")) for e in profile.get("education", [])])
    prof_exp = " ".join([normalize_text(e.get("job_title", "")) + " " + normalize_text(e.get("responsibilities", "")) for e in profile.get("experience", [])])

    # 2. Career Fit Engine (Deterministic Multi-Signal)
    career_fit_results = []
    
    for career_name, criteria in CAREER_TAXONOMY.items():
        # A. Skill Match (35%)
        req_skills = [normalize_text(s) for s in criteria["skills"]]
        matched_skills = [s for s in req_skills if s in prof_skills]
        skill_score = (len(matched_skills) / len(req_skills)) if req_skills else 0
        
        # B. Project Relevance (20%)
        # Calculate how many project keywords are hit across all projects
        req_proj = [normalize_text(k) for k in criteria.get("project_keywords", [])]
        proj_hits = 0
        matched_proj_keywords = set()
        for p in prof_projects:
            for k in req_proj:
                if k in p["text"] or k in p["techs"]:
                    proj_hits += 1
                    matched_proj_keywords.add(k)
        
        # Cap project score logic (if they hit 3+ keywords, give 100%)
        proj_score = min(1.0, len(matched_proj_keywords) / 3) if req_proj else 0
        
        # C. Education Relevance (10%)
        req_edu = [normalize_text(e) for e in criteria.get("education", [])]
        edu_score = 1.0 if any(e in prof_edu for e in req_edu) else 0.0
        
        # D. Experience Relevance (10%)
        req_exp = [normalize_text(e) for e in criteria.get("experience_keywords", [])]
        exp_score = 1.0 if any(e in prof_exp for e in req_exp) else 0.0
        
        # E. Semantic Similarity (20%)
        # Map career to its dataset category and get centroid similarity
        semantic_score = 0.0
        dataset_cat = criteria.get("dataset_category", "")
        if dataset_cat in prototypes:
            proto_tensor = torch.tensor(prototypes[dataset_cat])
            s_val = util.cos_sim(emb, proto_tensor)[0][0].item()
            semantic_score = max(0.0, s_val)
            
        # F. Classification Signal (5%)
        class_score = 1.0 if primary_category == dataset_cat else 0.0
        
        # Relevance Gate: Reject if Skill Match & Project Match are extremely low
        if skill_score < 0.2 and proj_score < 0.2:
            continue # Gate prevents unrelated careers
            
        # Calculate Total Fit (100%)
        total_fit = (
            (skill_score * 0.35) +
            (proj_score * 0.20) +
            (semantic_score * 0.20) +
            (edu_score * 0.10) +
            (exp_score * 0.10) +
            (class_score * 0.05)
        )
        
        career_fit_results.append({
            "career": career_name,
            "total_fit": round(total_fit * 100, 1),
            "breakdown": {
                "skill_match": round(skill_score * 100, 1),
                "project_match": round(proj_score * 100, 1),
                "semantic_match": round(semantic_score * 100, 1),
                "education_match": round(edu_score * 100, 1),
                "experience_match": round(exp_score * 100, 1),
                "classification_signal": round(class_score * 100, 1)
            },
            "evidence": {
                "matched_skills": criteria["skills"][:len(matched_skills)] if matched_skills else [],
                "missing_skills": [s for s in criteria["skills"] if normalize_text(s) not in matched_skills],
                "matched_projects": list(matched_proj_keywords)
            }
        })
        
    career_fit_results = sorted(career_fit_results, key=lambda x: x['total_fit'], reverse=True)[:5]
    
    output = {
        "classification": {
            "category": primary_category,
            "confidence": primary_confidence
        },
        "career_fit": career_fit_results,
        "similar_cvs": similar_cvs
    }
    
    return output

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    output = calculate_similarity(sys.argv[1])
    print("===START===")
    print(json.dumps(output))
    print("===END===")
