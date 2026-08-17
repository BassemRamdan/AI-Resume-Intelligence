"""
Deterministic Career Fit Engine.
Computes multi-signal candidate compatibility using strict mathematical weights:
  Skill Match: 35%
  Project Relevance: 20%
  Semantic Similarity: 20%
  Education Relevance: 10%
  Experience Relevance: 10%
  Classification Signal: 5%
Implements an Anti-Hallucination Relevance Gate to prevent false recommendations.
"""

import os
import json
import torch
import numpy as np
from sentence_transformers import util
from .taxonomy import CAREER_TAXONOMY
from ..models.embedder import get_embedder_model, get_embedding_resources, encode_text

def normalize_text(text) -> str:
    """Normalize text into lowercase tokens."""
    if isinstance(text, list):
        text = " ".join([str(x) for x in text])
    if not isinstance(text, str):
        text = str(text)
    return text.lower().strip() if text else ""

def calculate_career_fit(profile: dict, data_dir: str = None) -> dict:
    """
    Computes deterministic career recommendations and KNN similar resume benchmarks.
    """
    raw_text = profile.get("raw_text_snippet", "")
    primary_category = profile.get("career_signal", {}).get("dataset_category", "UNKNOWN")
    primary_confidence = profile.get("career_signal", {}).get("confidence", 0.0)
    
    embedder = get_embedder_model("cpu")
    cv_embeddings, cv_metadata, prototypes = get_embedding_resources(data_dir)
    
    # 1. Compute KNN Semantic Similar Resumes
    similar_cvs = []
    if cv_embeddings is not None and cv_metadata is not None:
        emb_tensor = torch.tensor(encode_text(raw_text, "cpu"))
        cv_embs_tensor = torch.tensor(cv_embeddings)
        cos_scores = util.cos_sim(emb_tensor, cv_embs_tensor)[0]
        top_results = torch.topk(cos_scores, k=min(3, len(cv_metadata)))
        
        for score, idx in zip(top_results[0], top_results[1]):
            match_meta = cv_metadata[idx.item()]
            s_val = score.item()
            mapped_score = round(max(0.0, min(100.0, s_val * 100.0)), 1)
            similar_cvs.append({
                "id": match_meta.get("id", idx.item()),
                "category": match_meta.get("category", "General"),
                "skills": match_meta.get("skills_preview", ""),
                "experience": match_meta.get("experience_preview", ""),
                "score": mapped_score
            })
            
    # 2. Extract Candidate Profile Attributes
    candidate_skills = set()
    for s in profile.get("skills") or []:
        s_name = normalize_text(s.get("name", ""))
        if s_name:
            candidate_skills.add(s_name)
            
    candidate_projects = []
    for p in profile.get("projects") or []:
        p_text = normalize_text(p.get("name", "")) + " " + normalize_text(p.get("description", ""))
        candidate_projects.append(p_text)
    combined_project_text = " ".join(candidate_projects)
    
    candidate_edu_text = " ".join([normalize_text(e.get("degree", "")) + " " + normalize_text(e.get("field", "")) for e in (profile.get("education") or [])])
    candidate_exp_text = " ".join([normalize_text(exp.get("job_title", "")) for exp in (profile.get("experience") or [])])
    
    candidate_emb = encode_text(raw_text, "cpu")
    
    # 3. Deterministic Career Fit Computation
    career_fit_results = []
    
    for career_name, criteria in CAREER_TAXONOMY.items():
        # A. Skill Match (35%)
        target_skills = [normalize_text(s) for s in criteria.get("skills", [])]
        matched_skills = [s for s in target_skills if s in candidate_skills]
        skill_score = len(matched_skills) / max(1, len(target_skills))
        
        # B. Project Match (20%)
        target_proj_keywords = [normalize_text(k) for k in criteria.get("project_keywords", [])]
        matched_projects = [k for k in target_proj_keywords if k in combined_project_text or any(k in p for p in candidate_projects)]
        project_score = len(matched_projects) / max(1, len(target_proj_keywords))
        
        # C. Semantic Match (20%)
        semantic_score = 0.0
        domain_cat = criteria.get("domain", "")
        if prototypes and domain_cat in prototypes:
            proto_vec = np.array(prototypes[domain_cat], dtype=np.float32)
            norm_c = np.linalg.norm(candidate_emb)
            norm_p = np.linalg.norm(proto_vec)
            if norm_c > 0 and norm_p > 0:
                sim = float(np.dot(candidate_emb, proto_vec) / (norm_c * norm_p))
                semantic_score = max(0.0, min(1.0, sim))
                
        # D. Education Match (10%)
        target_edu = [normalize_text(k) for k in criteria.get("education_keywords", [])]
        edu_score = 1.0 if any(k in candidate_edu_text for k in target_edu) else 0.0
        
        # E. Experience Match (10%)
        target_exp = [normalize_text(k) for k in criteria.get("experience_keywords", [])]
        exp_score = 1.0 if any(k in candidate_exp_text for k in target_exp) else 0.0
        
        # F. Classification Signal (5%)
        class_score = 0.0
        if primary_category and primary_category.upper() == domain_cat.upper():
            class_score = float(primary_confidence) if primary_confidence else 1.0
            
        # Anti-Hallucination Relevance Gate
        # If both direct skill match and project match are 0, penalize semantic overlap
        effective_semantic = semantic_score
        if skill_score == 0 and project_score == 0:
            effective_semantic = semantic_score * 0.20
            
        total_fit = (
            0.35 * skill_score +
            0.20 * project_score +
            0.20 * effective_semantic +
            0.10 * edu_score +
            0.10 * exp_score +
            0.05 * class_score
        )
        
        career_fit_results.append({
            "career": career_name,
            "total_fit": round(total_fit * 100.0, 1),
            "breakdown": {
                "skill_match": round(skill_score * 100.0, 1),
                "project_match": round(project_score * 100.0, 1),
                "semantic_match": round(effective_semantic * 100.0, 1),
                "education_match": round(edu_score * 100.0, 1),
                "experience_match": round(exp_score * 100.0, 1),
                "classification_signal": round(class_score * 100.0, 1)
            },
            "evidence": {
                "matched_skills": [s for s in criteria.get("skills", []) if normalize_text(s) in candidate_skills],
                "missing_skills": [s for s in criteria.get("skills", []) if normalize_text(s) not in candidate_skills],
                "matched_projects": matched_projects
            }
        })
        
    career_fit_results = sorted(career_fit_results, key=lambda x: x["total_fit"], reverse=True)[:5]
    
    return {
        "classification": {
            "category": primary_category,
            "confidence": primary_confidence
        },
        "career_fit": career_fit_results,
        "similar_cvs": similar_cvs
    }
