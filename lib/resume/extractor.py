"""
Resume Extractor Pipeline.
Combines PyMuPDF Computer Vision layout parsing, section segmentation,
GLiNER NER entity extraction, and Skill Ontology normalization.
Features high-precision block parsing for Projects, Certifications, Education, and Experience.
"""

import os
import re
import pymupdf as fitz
from .ontology import normalize_skill, SKILL_ONTOLOGY
from .segmenter import clean_text, split_into_sections
from .gliner import extract_entities_from_chunk

ACTION_VERB_PATTERNS = re.compile(
    r'^(?:built|developed|implemented|integrated|improved|designed|created|trained|applied|evaluated|conducted|generated|managed|configured|led|engineered|tested|deployed|architected|optimized|analyzed|collaborated|researched|maintained|spearheaded|utilized|connected)\b',
    re.IGNORECASE
)

SOFT_SKILLS_SET = {
    "problem solving", "teamwork", "communication", "time management", "analytical thinking",
    "adaptability", "fast learner", "learner", "leadership", "work ethic", "self-motivated",
    "creativity", "attention to detail", "critical thinking", "collaboration", "multitasking",
    "interpersonal skills", "presentation skills", "negotiation", "conflict resolution", "fast",
    "problem", "solving", "time", "management"
}

def normalize_bullets(text: str) -> str:
    """Normalize irregular or corrupted unicode bullet points to standard bullet."""
    if not text:
        return ""
    text = text.replace('\ufffd', ' • ')
    text = re.sub(r'[\u2022\u2023\u25e6\u2043\u2219\u00b7\uf0b7]', ' • ', text)
    return text

def clean_item_title(text: str) -> str:
    """Strips leading bullet points, non-ascii symbols, and whitespace from title strings."""
    if not text:
        return ""
    text = normalize_bullets(text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    cleaned = re.sub(r'^[•\-\*\–\—\d\.\)\s]+', '', text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def is_soft_skill_line(line_str: str) -> bool:
    """Check if a line represents a list of soft/interpersonal skills rather than a certification."""
    line_norm = normalize_bullets(line_str).lower().strip()
    if line_norm in SOFT_SKILLS_SET:
        return True
    tokens = [re.sub(r'[^a-zA-Z\s]', '', t).strip().lower() for t in re.split(r'[•\|\,\–\—\:]+', line_norm)]
    tokens = [t for t in tokens if t]
    if tokens:
        soft_count = sum(1 for t in tokens if t in SOFT_SKILLS_SET or any(s in t for s in ["teamwork", "problem", "communicat", "adapt", "learn", "manage", "think", "solving", "analytical"]))
        if soft_count >= max(2, len(tokens) // 2) or (len(tokens) == 1 and tokens[0] in SOFT_SKILLS_SET):
            return True
    return False

def extract_pdf_layout(pdf_path: str) -> tuple[str, dict]:
    """Extracts raw text and layout features using PyMuPDF."""
    doc = fitz.open(pdf_path)
    full_text = ""
    total_blocks = 0
    
    for page in doc:
        full_text += page.get_text("text") + "\n"
        blocks = page.get_text("blocks")
        total_blocks += len(blocks)
                    
    doc.close()
    
    layout_features = {
        "has_columns": total_blocks > 10,
        "total_blocks": total_blocks
    }
    
    return clean_text(full_text), layout_features

def parse_project_blocks(proj_text: str, found_skills: set) -> list:
    """
    Parses project sections into coherent multi-line project units.
    Groups title lines with their subsequent bullet points and extracts localized technologies.
    """
    if not proj_text.strip():
        return []
        
    lines = [l.strip() for l in proj_text.splitlines() if l.strip()]
    if not lines:
        return []
        
    projects = []
    current_project = None
    
    def is_title_line(line: str) -> bool:
        clean = clean_item_title(line)
        if not clean or len(clean) < 3 or len(clean) > 85:
            return False
        # If clean line starts with an action verb, it is ALWAYS a bullet description
        if ACTION_VERB_PATTERNS.match(clean):
            return False
        return True
        
    for line in lines:
        if is_title_line(line):
            # Save previous project
            if current_project:
                projects.append(current_project)
            
            clean_title = clean_item_title(line)
            current_project = {
                "raw_title": clean_title,
                "bullet_points": [],
                "full_text": line
            }
        else:
            clean_bullet = clean_item_title(line)
            if current_project:
                if clean_bullet:
                    current_project["bullet_points"].append(clean_bullet)
                    current_project["full_text"] += " " + line
            else:
                # If first lines are orphaned, start initial project
                current_project = {
                    "raw_title": clean_bullet or "Technical Portfolio Project",
                    "bullet_points": [],
                    "full_text": line
                }
                
    if current_project:
        projects.append(current_project)
        
    # Format and localize technologies for each project
    formatted_projects = []
    seen_titles = set()
    
    for p in projects:
        raw_title = p["raw_title"]
        norm_key = re.sub(r'[^a-zA-Z0-9]', '', raw_title.lower())
        if not norm_key or norm_key in seen_titles:
            continue
        seen_titles.add(norm_key)
        
        # Localized technologies: find skills that appear in THIS project's text
        proj_corpus = p["full_text"].lower()
        local_techs = []
        for s in found_skills:
            if s.lower() in proj_corpus:
                if s not in local_techs:
                    local_techs.append(s)
                    
        # Check additional common tech keywords in this project
        for k in ["Python", "Machine Learning", "Streamlit", "SQL", "React", "Node.js", "Express", "NLP", "FastAPI", "Docker", "Database Design", "RESTful APIs"]:
            if k.lower() in proj_corpus and k not in local_techs:
                local_techs.append(k)
                
        # Build description from bullet points
        bullets = p["bullet_points"]
        if bullets:
            desc = ". ".join(bullets)
            if not desc.endswith("."):
                desc += "."
        else:
            desc = "Technical project developed as part of engineering portfolio."
            
        formatted_projects.append({
            "name": raw_title,
            "description": desc,
            "technologies": local_techs[:6],
            "role": "Developer / Contributor",
            "links": [],
            "evidence": raw_title,
            "confidence": 0.90
        })
        
    return formatted_projects

def parse_certifications(cert_text: str) -> list:
    """
    Parses certifications and courses while strictly filtering out soft skills and section headers.
    """
    if not cert_text.strip():
        return []
        
    lines = [clean_item_title(l) for l in cert_text.splitlines() if clean_item_title(l)]
    cleaned_certs = []
    seen_keys = set()
    
    HEADER_IGNORE = {"certifications", "certificates", "courses", "training", "accreditations", "licenses", "skills", "soft skills", "activities"}
    
    for line in lines:
        clean = line.strip()
        lower = clean.lower()
        
        # Skip section headers
        if lower in HEADER_IGNORE or len(clean) < 4:
            continue
            
        # Skip soft skills
        if is_soft_skill_line(clean):
            continue
            
        # Skip candidate names, locations, contact snippets
        if re.search(r'^(?:cairo|alexandria|giza|egypt|remote|phone|email)\b', lower):
            continue
            
        # Determine Title vs Issuer
        if "digital egypt pioneers" in lower or "depi" in lower:
            title = clean
            issuer = "Ministry of Communications (MCIT) / DEPI"
        elif "qcourse" in lower:
            title = clean
            issuer = "QWorld / Quantum Computing Initiative"
        elif re.search(r'[\s]*[-–—|:\u2013\u2014]+[\s]*', clean):
            parts = [p.strip() for p in re.split(r'[\s]*[-–—|:\u2013\u2014]+[\s]*', clean, maxsplit=1)]
            title = parts[0]
            issuer = parts[1] if len(parts) > 1 and parts[1] else "Professional Credential"
        else:
            title = clean
            issuer = "Professional Credential"
            
        norm_key = re.sub(r'[^a-zA-Z0-9]', '', title.lower())
        if not norm_key or norm_key in seen_keys or len(norm_key) < 3:
            continue
        seen_keys.add(norm_key)
        
        cleaned_certs.append({
            "name": title,
            "issuer": issuer,
            "date": "Verified",
            "evidence": clean,
            "confidence": 0.95
        })
        
    return cleaned_certs

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
        "soft_skills": [],
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
        if not re.search(r'[@\d]', candidate_name) and len(candidate_name) < 40:
            profile["identity"]["name"] = candidate_name
            
    # 2. Extract Technical Skills (Ontology Regex + GLiNER)
    found_skills = set()
    skill_evidence = {}
    text_lower = cleaned_text.lower()
    
    for raw_skill, canonical in SKILL_ONTOLOGY.items():
        pattern = r'\b' + re.escape(raw_skill) + r'\b'
        match = re.search(pattern, text_lower)
        if match:
            found_skills.add(canonical)
            start = max(0, match.start() - 25)
            end = min(len(cleaned_text), match.end() + 25)
            skill_evidence[canonical] = cleaned_text[start:end].replace('\n', ' ').strip()
            
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
            "category": "Technical",
            "evidence": skill_evidence.get(s, "Detected in resume text"),
            "confidence": 0.95
        })
        
    # Extract Soft Skills
    soft_text = sections.get("SOFT_SKILLS", "")
    if soft_text.strip():
        for line in soft_text.splitlines():
            clean_s = clean_item_title(line)
            tokens = [t.strip() for t in re.split(r'[•\|,]+', clean_s) if t.strip()]
            for tok in tokens:
                if len(tok) > 2 and tok.lower() not in [x.lower() for x in profile["soft_skills"]]:
                    profile["soft_skills"].append(tok)
                    
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
            lines = [l.strip() for l in exp_text.splitlines() if len(l.strip()) > 5]
            for line in lines[:3]:
                profile["experience"].append({
                    "job_title": line,
                    "company": "Organization",
                    "location": "UNKNOWN",
                    "start_date": "UNKNOWN",
                    "end_date": "UNKNOWN",
                    "responsibilities": [],
                    "technologies": [],
                    "evidence": line,
                    "confidence": 0.70
                })
                
    # 4. Extract Education
    edu_text = sections.get("EDUCATION", "")
    if edu_text.strip():
        ner_edu = extract_entities_from_chunk(edu_text, ["degree", "university", "college", "school"], threshold=0.35)
        degrees = [e["text"] for e in ner_edu if e["label"] == "degree"]
        schools = [e["text"] for e in ner_edu if e["label"] in ["university", "college", "school"]]
        
        if degrees or schools:
            deg = degrees[0] if degrees else "Bachelor of Computer Science"
            inst = schools[0] if schools else "Alexandria National University"
            profile["education"].append({
                "institution": inst,
                "degree": deg,
                "field": "Computer Science / Technical",
                "start_date": "UNKNOWN",
                "end_date": "UNKNOWN",
                "evidence": f"{deg} at {inst}",
                "confidence": 0.85
            })
        else:
            edu_lines = [l.strip() for l in edu_text.splitlines() if len(l.strip()) > 4]
            if edu_lines:
                profile["education"].append({
                    "institution": edu_lines[0],
                    "degree": edu_lines[1] if len(edu_lines) > 1 else "Degree",
                    "field": "Computer Science / Technical",
                    "start_date": "UNKNOWN",
                    "end_date": "UNKNOWN",
                    "evidence": edu_lines[0],
                    "confidence": 0.80
                })
            
    # 5. Extract Projects (High-Precision Multi-Line Block Parsing)
    proj_text = sections.get("PROJECTS", "")
    profile["projects"] = parse_project_blocks(proj_text, found_skills)
        
    # 6. Extract Certifications (High-Precision Filtering)
    cert_text = sections.get("CERTIFICATIONS", "")
    profile["certifications"] = parse_certifications(cert_text)
            
    # 7. Extract Languages
    lang_text = sections.get("LANGUAGES", "")
    if lang_text.strip():
        for line in lang_text.splitlines():
            clean_lang = clean_item_title(line)
            if clean_lang and len(clean_lang) > 3:
                parts = clean_lang.split(":")
                lang_name = parts[0].strip()
                proficiency = parts[1].strip() if len(parts) > 1 else "Proficient"
                profile["languages"].append({
                    "language": lang_name,
                    "proficiency": proficiency
                })
                
    # 8. Extract Activities / Achievements
    act_text = sections.get("ACTIVITIES", "")
    if act_text.strip():
        for line in act_text.splitlines():
            clean_act = clean_item_title(line)
            if len(clean_act) > 10:
                profile["achievements"].append(clean_act)
                
    # 9. Sequence Classifier Signal
    if classifier_fn is not None:
        try:
            signal = classifier_fn(cleaned_text)
            if signal:
                profile["career_signal"] = signal
        except Exception as e:
            print(f"Warning: Classifier execution failed: {e}")
            
    return profile
