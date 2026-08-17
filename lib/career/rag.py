"""
Career Roadmap RAG (Retrieval-Augmented Generation) Engine.
Indexes expert career roadmaps, senior milestones, portfolio project blueprints,
and skill gap solutions using SentenceTransformers dense semantic embeddings.
"""

import os
import json
import numpy as np
from ..models.embedder import get_embedder_model

_RAG_INDEX = None

def _load_and_index_kb():
    """Loads roadmap metadata and generates dense embeddings for fast semantic retrieval."""
    global _RAG_INDEX
    if _RAG_INDEX is not None:
        return _RAG_INDEX

    kb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "career_roadmaps_kb.json")
    if not os.path.exists(kb_path):
        kb_path = os.path.join("data", "career_roadmaps_kb.json")

    with open(kb_path, "r", encoding="utf-8") as f:
        kb_data = json.load(f)

    chunks = []
    chunk_metadata = []

    for domain, roles in kb_data.items():
        for role_name, details in roles.items():
            # 1. Overview & Seniority Chunk
            seniority_text = " ".join([f"{k} Level: {v}" for k, v in details.get("seniority_levels", {}).items()])
            chunks.append(f"Career Role: {role_name} ({domain})\nOverview: {details.get('overview', '')}\nSeniority Milestones: {seniority_text}")
            chunk_metadata.append({"role": role_name, "domain": domain, "type": "overview_seniority"})

            # 2. Tech Stack & Foundational Skills Chunk
            found_skills = ", ".join(details.get("foundational_skills", []))
            applied_skills = ", ".join(details.get("applied_tech_stack", []))
            chunks.append(f"Career Role: {role_name} ({domain})\nFoundational Competencies: {found_skills}\nApplied Technical Stack: {applied_skills}")
            chunk_metadata.append({"role": role_name, "domain": domain, "type": "tech_stack"})

            # 3. Must-Build Portfolio Projects Chunk
            projs = details.get("must_build_projects", [])
            proj_str = "\n".join([f"- Project Title: {p['title']}\n  Description: {p['description']}\n  Key Tech: {', '.join(p.get('tech', []))}" for p in projs])
            chunks.append(f"Career Role: {role_name} ({domain})\nRecommended Portfolio Project Blueprints:\n{proj_str}")
            chunk_metadata.append({"role": role_name, "domain": domain, "type": "projects"})

            # 4. Certifications, Skill Gaps & Interview Prep Chunk
            certs = ", ".join([f"{c['name']} (ROI: {c.get('roi', 'High')})" for c in details.get("recommended_certifications", [])])
            gaps = " ".join(details.get("high_value_skill_gaps", []))
            interviews = ", ".join(details.get("common_interview_topics", []))
            chunks.append(f"Career Role: {role_name} ({domain})\nHigh-ROI Certifications: {certs}\nCommon Skill Pitfalls & Gaps: {gaps}\nKey Interview Assessment Topics: {interviews}")
            chunk_metadata.append({"role": role_name, "domain": domain, "type": "interview_certs_gaps"})

            # 5. Roadmap Phases Chunk
            roadmap = details.get("roadmap", {})
            if roadmap:
                r_str = f"Phase 1 (Foundations): {roadmap.get('phase_1', '')}\nPhase 2 (Applied Projects): {roadmap.get('phase_2', '')}\nPhase 3 (Production Mastery): {roadmap.get('phase_3', '')}"
                chunks.append(f"Career Role: {role_name} ({domain})\nStep-by-Step Learning Roadmap:\n{r_str}")
                chunk_metadata.append({"role": role_name, "domain": domain, "type": "roadmap"})

    # Compute dense embeddings using SentenceTransformer model
    embedder = get_embedder_model("cpu")
    embeddings = embedder.encode(chunks, show_progress_bar=False, normalize_embeddings=True)

    _RAG_INDEX = {
        "chunks": chunks,
        "metadata": chunk_metadata,
        "embeddings": np.array(embeddings, dtype=np.float32)
    }
    return _RAG_INDEX

def retrieve_roadmap_context(query: str, target_career: str = None, top_k: int = 3) -> str:
    """
    Performs semantic cosine retrieval over the expert career roadmap knowledge base.
    Returns formatted context block for LLM prompt augmentation.
    """
    try:
        index = _load_and_index_kb()
        embedder = get_embedder_model("cpu")

        # Augment search query with target career name if provided
        search_query = f"{target_career} {query}" if target_career else query
        query_vec = embedder.encode([search_query], show_progress_bar=False, normalize_embeddings=True)[0]

        # Cosine similarity (vectors are L2 normalized, so dot product = cosine similarity)
        scores = np.dot(index["embeddings"], query_vec)

        # Prefer chunks from target career if specified
        if target_career:
            for idx, meta in enumerate(index["metadata"]):
                if meta["role"].lower() == target_career.lower() or meta["domain"].lower() in target_career.lower():
                    scores[idx] += 0.35  # Relevance boost for target domain

        top_indices = np.argsort(scores)[::-1][:top_k]

        retrieved_texts = []
        for idx in top_indices:
            retrieved_texts.append(index["chunks"][idx])

        return "\n\n---\n\n".join(retrieved_texts)
    except Exception as e:
        print(f"RAG retrieval warning: {e}")
        return ""
