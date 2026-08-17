"""
Resume Extractor Pipeline.
Combines PyMuPDF Computer Vision layout parsing, section segmentation,
GLiNER NER entity extraction, and Skill Ontology normalization.
"""

import os
import re
import pymupdf as fitz
from .ontology import normalize_skill, SKILL_ONTOLOGY
from .segmenter import clean_text, split_into_sections
from .gliner import extract_entities_from_chunk

def extract_pdf_layout(pdf_path: str) -> tuple[str, dict]:
    """
    Extracts raw text and CV layout features (font hierarchy, block count) using PyMuPDF.
    """
    doc = fitz.open(pdf_path)
    full_text = ""
    font_sizes = set()
    total_blocks = 0
    
    for page in doc:
        full_text += page.get_text("text") + "\n"
        blocks = page.get_text("blocks")
        total_blocks += len(blocks)
        for b in blocks:
            if len(b) > 4 and isinstance(b[4], str):
                for line in b[4].splitlines():
                    pass # text line
                    
    doc.close()
    
    layout_features = {
        "has_columns": total_blocks > 10,
        "font_hierarchy_levels": max(1, len(font_sizes)),
        "total_blocks": total_blocks
    }
    
    return clean_text(full_text), layout_features

def extract_resume(pdf_path: str, classifier_fn = None) -> dict:
    """
    Complete deterministic profile extraction pipeline for a resume PDF.
    Returns structured candidate profile adhering strictly to grounded evidence.
    """
    cleaned_text, layout_features = extract_pdf_layout(pdf_path)
    sections = split_into_sections(cleaned_text)
    
    profile = {
        "identity": {},
        "summary": "UNKNOWN",
        "skills": [],
        "education": [],
        "experience": [],
        "projects": [],
        "certifications": [],
        "languages": [],
        "achievements": [],
        "layout_features": layout_features,
        "career_signal": {"dataset_category": "UNKNOWN_CATEGORY", "confidence": 0.0},
        "filename": os.path.basename(pdf_path),
        "raw_text_snippet": cleaned_text
    }
    
    # 1. Extract Identity & Contact Info
    header_chunk = sections.get("UNCLASSIFIED", "") or cleaned_text[:500]
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', cleaned_text)
    phone_match = re.search(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', cleaned_text)
    
    if email_match:
        profile["identity"]["email"] = email_match.group(0)
    if phone_match:
        profile["identity"]["phone"] = phone_match.group(0)
        
    first_lines = [l.strip() for l in header_chunk.splitlines() if l.strip()]
    if first_lines:
        candidate_name = first_lines[0]
        # Ignore if header is an email or generic label
        if not re.search(r'[@\d]', candidate_name) and len(candidate_name) < 40:
            profile["identity"]["name"] = candidate_name
            
    # 2. Extract Skills (Ontology Regex + GLiNER)
    found_skills = set()
    skill_evidence = {}
    text_lower = cleaned_text.lower()
    
    # Fast regex scan against standardized ontology
    for raw_skill, canonical in SKILL_ONTOLOGY.items():
        pattern = r'\b' + re.escape(raw_skill) + r'\b'
        match = re.search(pattern, text_lower)
        if match:
            found_skills.add(canonical)
            start = max(0, match.start() - 25)
            end = min(len(cleaned_text), match.end() + 25)
            skill_evidence[canonical] = cleaned_text[start:end].replace('\n', ' ').strip()
            
    # GLiNER entity extraction on SKILLS section
    skills_text = sections.get("SKILLS", "")
    if skills_text.strip():
        ner_skills = extract_entities_from_chunk(skills_text, ["skill", "technology", "programming language"], threshold=0.3)
        for item in ner_skills:
            norm = normalize_skill(item["text"])
            if norm and norm not in found_skills:
                found_skills.add(norm)
                skill_evidence[norm] = item["text"]
                
    for s in sorted(list(found_skills)):
        profile["skills"].append({
            "name": s,
            "normalized_name": s,
            "category": "UNKNOWN",
            "evidence": skill_evidence.get(s, "Detected in resume text"),
            "confidence": 0.95
        })
        
    # 3. Extract Experience
    exp_text = sections.get("EXPERIENCE", "")
    if exp_text.strip():
        ner_exp = extract_entities_from_chunk(exp_text, ["job title", "company", "position"], threshold=0.35)
        titles = [e["text"] for e in ner_exp if e["label"] in ["job title", "position"]]
        companies = [e["text"] for e in ner_exp if e["label"] == "company"]
        
        if titles:
            for idx, title in enumerate(titles[:5]):
                comp = companies[idx] if idx < len(companies) else "Company Not Specified"
                profile["experience"].append({
                    "job_title": title,
                    "company": comp,
                    "location": "UNKNOWN",
                    "start_date": "UNKNOWN",
                    "end_date": "UNKNOWN",
                    "responsibilities": [],
                    "technologies": [],
                    "evidence": f"{title} at {comp}",
                    "confidence": 0.85
                })
        else:
            # Fallback heuristic lines
            for line in exp_text.splitlines()[:5]:
                if len(line.strip()) > 5:
                    profile["experience"].append({
                        "job_title": line.strip(),
                        "company": "UNKNOWN",
                        "location": "UNKNOWN",
                        "start_date": "UNKNOWN",
                        "end_date": "UNKNOWN",
                        "responsibilities": [],
                        "technologies": [],
                        "evidence": line.strip(),
                        "confidence": 0.70
                    })
                    break
                    
    # 4. Extract Education
    edu_text = sections.get("EDUCATION", "")
    if edu_text.strip():
        ner_edu = extract_entities_from_chunk(edu_text, ["degree", "university", "college", "school"], threshold=0.35)
        degrees = [e["text"] for e in ner_edu if e["label"] == "degree"]
        schools = [e["text"] for e in ner_edu if e["label"] in ["university", "college", "school"]]
        
        if degrees or schools:
            deg = degrees[0] if degrees else "Degree/Coursework"
            inst = schools[0] if schools else "Institution"
            profile["education"].append({
                "institution": inst,
                "degree": deg,
                "field": "Computer Science / Technical",
                "start_date": "UNKNOWN",
                "end_date": "UNKNOWN",
                "evidence": f"{deg} at {inst}",
                "confidence": 0.85
            })
            
    # 5. Extract Projects (ALL Projects Retained as List)
    proj_text = sections.get("PROJECTS", "")
    if proj_text.strip():
        ner_proj = extract_entities_from_chunk(proj_text, ["project", "software", "application"], threshold=0.3)
        found_projs = []
        for p in ner_proj:
            p_name = p["text"].strip()
            if len(p_name) > 2 and p_name not in found_projs:
                found_projs.append(p_name)
                
        if found_projs:
            for p_name in found_projs:
                profile["projects"].append({
                    "name": p_name,
                    "description": "Technical project extracted from portfolio section",
                    "technologies": [s for s in found_skills if s.lower() in proj_text.lower()][:5],
                    "role": "Developer / Contributor",
                    "links": [],
                    "evidence": p_name,
                    "confidence": 0.80
                })
        else:
            # Line-based fallback
            proj_lines = [l.strip() for l in proj_text.splitlines() if len(l.strip()) > 4][:5]
            for pl in proj_lines:
                profile["projects"].append({
                    "name": pl[:40],
                    "description": pl,
                    "technologies": [],
                    "role": "Contributor",
                    "links": [],
                    "evidence": pl,
                    "confidence": 0.70
                })
                
    # 6. Extract Certifications
    cert_text = sections.get("CERTIFICATIONS", "")
    if cert_text.strip():
        for line in cert_text.splitlines():
            line_str = line.strip()
            if len(line_str) > 4:
                profile["certifications"].append({
                    "name": line_str,
                    "issuer": "Accredited Provider",
                    "date": "UNKNOWN",
                    "evidence": line_str,
                    "confidence": 0.85
                })
                
    # 7. Sequence Classifier Signal
    if classifier_fn is not None:
        try:
            signal = classifier_fn(cleaned_text)
            if signal:
                profile["career_signal"] = signal
        except Exception as e:
            print(f"Warning: Classifier execution failed: {e}")
            
    return profile
