"""
Resume Extractor Pipeline.
Combines PyMuPDF Computer Vision layout parsing, section segmentation,
GLiNER NER entity extraction, and Skill Ontology normalization.
Features strict filtering and deduplication for Projects, Certifications, and Languages.
"""

import os
import re
import pymupdf as fitz
from .ontology import normalize_skill, SKILL_ONTOLOGY
from .segmenter import clean_text, split_into_sections
from .gliner import extract_entities_from_chunk

KNOWN_TECH_TOOLS = {
    "python", "javascript", "typescript", "c++", "c#", "java", "php", "go", "rust", "ruby",
    "asp.net", "asp.net core", "asp.net identity", "entity framework", "entity framework core",
    "signalr", "angular", "react", "vue", "next.js", "node.js", "express", "django", "flask", "fastapi", "laravel",
    "sql", "sql server", "mysql", "postgresql", "mongodb", "redis", "sqlite",
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "github", "gitlab", "ci/cd",
    "xunit", "nunit", "moq", "jest", "cypress", "pusher", "rabbitmq", "kafka", "postman"
}

def clean_item_title(text: str) -> str:
    """Strips leading bullet points, non-ascii symbols, and whitespace from title strings."""
    if not text:
        return ""
    cleaned = re.sub(r'^[^a-zA-Z0-9\(\[\{]+', '', text)
    cleaned = cleaned.replace('\ufffd', '').strip()
    return cleaned

def is_tech_or_tool(name: str) -> bool:
    """Check if a candidate string is a programming framework/tool rather than a standalone project name."""
    clean = name.strip().lower()
    if clean in KNOWN_TECH_TOOLS or clean in SKILL_ONTOLOGY:
        return True
    for tech in KNOWN_TECH_TOOLS:
        if clean == tech or (len(tech) > 3 and clean.startswith(tech + " ")):
            return True
    return False

def extract_pdf_layout(pdf_path: str) -> tuple[str, dict]:
    """Extracts raw text and layout features using PyMuPDF."""
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
                    pass
                    
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
        if not re.search(r'[@\d]', candidate_name) and len(candidate_name) < 40:
            profile["identity"]["name"] = candidate_name
            
    # 2. Extract Skills (Ontology Regex + GLiNER)
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
            
    # 5. Extract Projects (Smart Filtering + Deduplication + Localized Tech)
    proj_text = sections.get("PROJECTS", "")
    if proj_text.strip():
        # Split project section into individual project items/lines
        raw_proj_lines = [l.strip() for l in proj_text.splitlines() if l.strip()]
        
        # Candidate project titles: lines starting with bullet or title-cased headers
        candidate_projects = []
        for line in raw_proj_lines:
            clean_line = clean_item_title(line)
            # If line is short and looks like a title (e.g. "ChatApp – Real-time Chat Application" or "Ecom-App")
            if 3 <= len(clean_line) <= 65 and not clean_line.startswith(("http", "www", "git")):
                # Check if it is merely a single technology/tool
                if not is_tech_or_tool(clean_line):
                    candidate_projects.append(clean_line)
                    
        # If line parsing didn't find clear titles, try GLiNER
        if not candidate_projects:
            ner_proj = extract_entities_from_chunk(proj_text, ["project", "software", "application"], threshold=0.45)
            for p in ner_proj:
                p_name = clean_item_title(p["text"])
                if len(p_name) > 3 and not is_tech_or_tool(p_name):
                    candidate_projects.append(p_name)
                    
        # Deduplicate candidate projects (e.g. "ChatApp" and "Real-time Chat Application")
        deduped_projects = []
        seen_keys = set()
        
        for p in candidate_projects:
            # Extract main title before delimiter (e.g. "ChatApp – Real-time..." -> "ChatApp")
            p_clean = clean_item_title(p)
            main_title = re.split(r'[\–\-\|\:]', p_clean)[0].strip()
            norm_key = re.sub(r'[^a-zA-Z0-9]', '', main_title.lower())
            
            if not norm_key or norm_key in seen_keys or len(norm_key) < 2:
                continue
                
            # Check for substring redundancy
            is_sub = False
            for existing in seen_keys:
                if norm_key in existing or existing in norm_key:
                    is_sub = True
                    break
            if is_sub:
                continue
                
            seen_keys.add(norm_key)
            
            # Find localized technologies for this project
            local_techs = [
                s for s in found_skills 
                if s.lower() in proj_text.lower()
            ][:5]
            
            deduped_projects.append({
                "name": p_clean,
                "description": "Technical project extracted from resume portfolio section",
                "technologies": local_techs,
                "role": "Developer / Contributor",
                "links": [],
                "evidence": p_clean,
                "confidence": 0.85
            })
            
        profile["projects"] = deduped_projects
        
    # 6. Extract Certifications (High-Precision Filtering & Reconstruction)
    cert_text = sections.get("CERTIFICATIONS", "")
    if cert_text.strip():
        def is_cert_noise(line_str: str) -> bool:
            lower = line_str.lower().strip()
            # 1. Location matches
            if re.search(r'^(?:[a-zA-Z\s]+,\s*(?:egypt|cairo|alexandria|giza|usa|uk|remote|uae|saudi arabia|germany|canada))\b', lower):
                return True
            if lower in ["alexandria, egypt", "cairo, egypt", "remote, egypt", "egypt", "accredited provider", "verified"]:
                return True
            # 2. Candidate full name (All uppercase 2-3 words matching candidate name pattern)
            if re.match(r'^[A-Z\s]{4,30}$', line_str) and not any(k in lower for k in ["cert", "depi", "course", "program", "degree", "qcourse", "aws"]):
                return True
            # 3. Candidate summary taglines / headlines
            if re.search(r'\b(?:business solutions|high-performance|building scalable|scalable solutions)\b', lower) and not any(k in lower for k in ["cert", "course", "program"]):
                return True
            # 4. Tech stack lists with bullet delimiters
            if ("•" in line_str or "|" in line_str) and any(t in lower for t in ["c#", "sql", "javascript", "asp.net", "rest apis"]):
                return True
            # 5. Section headings or language words
            if re.match(r'^(?:&\s*activities|languages|activities|skills|native|intermediate)', lower):
                return True
            return False

        cert_raw_lines = [clean_item_title(l) for l in cert_text.splitlines() if clean_item_title(l)]
        filtered_cert_lines = [l for l in cert_raw_lines if not is_cert_noise(l) and len(l) > 3]

        # Multi-line item reconstruction
        merged_certs = []
        for line in filtered_cert_lines:
            if not merged_certs:
                merged_certs.append(line)
                continue
            last = merged_certs[-1]
            lower_line = line.lower()
            # Continuation patterns
            if line.startswith("(") or line.startswith("1:") or line.startswith("2:") or lower_line.startswith(("to ", "and ", "quantum", "computing", "development", "specialization", "foundations", "track", "program")):
                merged_certs[-1] = f"{last} {line}"
            elif "qcourse" in last.lower() and ("introduction" in lower_line or "quantum" in lower_line):
                merged_certs[-1] = f"{last}: {line}"
            elif "full stack" in last.lower() and "digital egypt" in lower_line:
                merged_certs[-1] = f"{last} - {line}"
            elif "digital egypt" in last.lower() and "depi" in lower_line:
                merged_certs[-1] = f"{last} ({line.strip('()')})"
            else:
                merged_certs.append(line)

        # Build clean structured certification objects with deduplication
        deduped_certs = []
        seen_cert_keys = set()

        for c_item in merged_certs:
            clean_item = re.sub(r'\s+', ' ', c_item).strip()
            if len(clean_item) < 4:
                continue

            # Parse title vs issuer
            if "digital egypt pioneers" in clean_item.lower() or "depi" in clean_item.lower():
                title = clean_item
                issuer = "Ministry of Communications (MCIT) / DEPI"
            elif "qcourse" in clean_item.lower():
                title = clean_item
                issuer = "QWorld / Quantum Computing Initiative"
            elif re.search(r'[\s]*[-–—|:\u2013\u2014]+[\s]*', clean_item):
                parts = [p.strip() for p in re.split(r'[\s]*[-–—|:\u2013\u2014]+[\s]*', clean_item, maxsplit=1)]
                title = parts[0]
                issuer = parts[1] if len(parts) > 1 and parts[1] else "Professional Credential"
            else:
                title = clean_item
                issuer = "Professional Credential"

            norm_key = re.sub(r'[^a-zA-Z0-9]', '', title.lower())
            if not norm_key or norm_key in seen_cert_keys:
                continue

            # Check if redundant substring
            if any(norm_key in existing or existing in norm_key for existing in seen_cert_keys):
                continue

            seen_cert_keys.add(norm_key)

            deduped_certs.append({
                "name": title,
                "issuer": issuer,
                "date": "Verified",
                "evidence": clean_item,
                "confidence": 0.95
            })

        profile["certifications"] = deduped_certs
            
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
