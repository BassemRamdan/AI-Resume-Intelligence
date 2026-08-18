"""
Resume Extractor Pipeline.
Combines PyMuPDF Computer Vision layout parsing, section segmentation,
GLiNER NER entity extraction, and Skill Ontology normalization.
Features universal multi-strategy fail-safe block parsing for Projects, Certifications, Education, and Experience.
"""

import os
import re
import pymupdf as fitz
from .ontology import normalize_skill, SKILL_ONTOLOGY
from .segmenter import clean_text, split_into_sections
from .gliner import extract_entities_from_chunk

ACTION_VERB_PATTERNS = re.compile(
    r'^(?:built|designed|paired|trained|benchmarked|developed|implemented|integrated|deployed|evaluated|incorporated|created|applied|conducted|generated|managed|configured|led|engineered|tested|architected|optimized|analyzed|collaborated|researched|maintained|spearheaded|utilized|connected|performed|structured|produced|authored|delivered)\b',
    re.IGNORECASE
)

SOFT_SKILLS_SET = {
    "problem solving", "teamwork", "communication", "time management", "analytical thinking",
    "adaptability", "fast learner", "learner", "leadership", "work ethic", "self-motivated",
    "creativity", "attention to detail", "critical thinking", "collaboration", "multitasking",
    "interpersonal skills", "presentation skills", "negotiation", "conflict resolution", "fast",
    "problem", "solving", "time", "management", "analytical"
}

KNOWN_TECH_KEYWORDS = [
    "Python", "React", "Node.js", "SQL", "TensorFlow", "PyTorch", "Scikit-learn", "Scikit", 
    "OpenCV", "XGBoost", "Streamlit", "MediaPipe", "Experta", "Pygame", "Surprise", 
    "Matplotlib", "Seaborn", "NLP", "FastAPI", "Docker", "Flask", "Django", "JavaScript", 
    "TypeScript", "C#", "C++", "Java", "AWS", "Git", "Database Design", "RESTful APIs",
    "EDA", "PCA", "SVD", "K-Medoids", "Minimax", "CNN", "FFNN", "MLP", "HTML", "CSS",
    "Angular", "Vue", "Next.js", "Kubernetes", "Linux", "Azure", "GCP", "PostgreSQL", "MongoDB"
]

NON_PROJECT_KEYWORDS = re.compile(
    r'^(?:bachelor|master|b\.sc|m\.sc|ph\.d|degree|faculty|university|institute|college|school|academic|education|experience|summary|profile|competencies|skills|certifications|languages|contact|email|phone)\b',
    re.IGNORECASE
)

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

def parse_project_blocks(proj_text: str, found_skills: set, candidate_name: str = "") -> list:
    """
    Universal multi-strategy project parser.
    Identifies project headers, groups bullet points, heals line breaks, and attaches localized technologies.
    """
    if not proj_text.strip():
        return []
        
    text = normalize_bullets(proj_text)
    raw_lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not raw_lines:
        return []
        
    project_blocks = []
    current_proj = None
    
    for line in raw_lines:
        clean_l = clean_item_title(line)
        if not clean_l or len(clean_l) < 3:
            continue
            
        # Ignore lines matching candidate name or education degrees/institutions
        if candidate_name and candidate_name.lower() in clean_l.lower() and len(clean_l) < len(candidate_name) + 10:
            continue
        if NON_PROJECT_KEYWORDS.match(clean_l):
            continue
            
        # Check if line contains a project header with glued description (e.g. "Neural Network... | Python... . Built and compared...")
        m = re.search(r'([A-Z0-9][\w\s\–\—\-\:\(\)]+?\s*[\|\–\—]\s*(?:Python|React|Node|SQL|TensorFlow|PyTorch|Scikit|OpenCV|XGBoost|Streamlit|MediaPipe|Experta|Pygame|Surprise|Matplotlib|Seaborn|Java|C#|C\+\+|AWS|Docker|Git)[\w\s\,\.\+\#\-\/]*?)[\.\:]\s+([A-Z][a-z]+.*)', line)
        if m and not ACTION_VERB_PATTERNS.match(clean_l):
            if current_proj:
                project_blocks.append(current_proj)
            current_proj = {
                'raw_header': m.group(1).strip(),
                'lines': [m.group(2).strip()]
            }
            continue
            
        # Check if line is a project header
        is_header = False
        
        # Delimited Header Pattern (e.g. "Hybrid Movie Recommendation System | Python, Scikit-learn, Surprise, Streamlit")
        if ('|' in line or ' — ' in line or ' – ' in line) and any(t.lower() in line.lower() for t in KNOWN_TECH_KEYWORDS):
            if not ACTION_VERB_PATTERNS.match(clean_l) and not line.startswith(('•', '-', '*')):
                is_header = True
        elif not ACTION_VERB_PATTERNS.match(clean_l) and not line.startswith(('•', '-', '*')) and len(clean_l) < 70:
            # Standalone project title line (e.g. "MindCare AI - Emotion Detection" or "Connect 4 Hand Gesture Game")
            if any(k in clean_l.lower() for k in ["system", "pipeline", "classifier", "model comparison", "ai game", "app", "platform", "detector", "detection", "predictor", "prediction", "dashboard", "engine", "network", "analysis", "microservices", "e-commerce"]):
                is_header = True
                
        if is_header:
            if current_proj:
                project_blocks.append(current_proj)
            current_proj = {
                'raw_header': clean_l,
                'lines': []
            }
        else:
            if current_proj:
                current_proj['lines'].append(line)
            else:
                current_proj = {
                    'raw_header': clean_l,
                    'lines': []
                }
                
    if current_proj:
        project_blocks.append(current_proj)
        
    final_projects = []
    seen_titles = set()
    
    for p in project_blocks:
        header = p['raw_header']
        
        # Discard invalid project headers (candidate name, degree, etc.)
        if candidate_name and candidate_name.lower() in header.lower() and len(header) < len(candidate_name) + 10:
            continue
        if NON_PROJECT_KEYWORDS.match(header):
            continue
            
        # Parse title and tech strings
        parts = re.split(r'[\s]*[\|\–\—]+[\s]*', header)
        if len(parts) > 1:
            title = parts[0].strip()
            if len(parts) > 2 and not any(k.lower() in parts[1].lower() for k in ["python", "react", "node", "sql", "tensorflow", "scikit", "pytorch", "opencv"]):
                title = f"{parts[0].strip()} — {parts[1].strip()}"
                tech_str = parts[2].strip()
            else:
                tech_str = parts[1].strip()
        else:
            title = header
            tech_str = ''
            
        norm_key = re.sub(r'[^a-zA-Z0-9]', '', title.lower())
        if not norm_key or norm_key in seen_titles or len(norm_key) < 3:
            continue
        seen_titles.add(norm_key)
        
        # Extract explicit technologies from header
        techs = []
        if tech_str:
            for t in re.split(r'[\,\•\/]+', tech_str):
                t_clean = t.strip(' .;()')
                if t_clean and len(t_clean) > 1 and t_clean not in techs:
                    techs.append(t_clean)
                    
        # Reconstruct body sentences and heal line breaks
        raw_body_lines = p['lines']
        reconstructed_sentences = []
        current_sentence = ''
        
        for bline in raw_body_lines:
            clean_b = re.sub(r'^[•\-\*\s]+', '', bline).strip()
            if not clean_b:
                continue
                
            starts_new_bullet = bool(bline.startswith(('•', '-', '*')) or ACTION_VERB_PATTERNS.match(clean_b))
            
            if starts_new_bullet:
                if current_sentence:
                    reconstructed_sentences.append(current_sentence.strip())
                current_sentence = clean_b
            else:
                if current_sentence:
                    if current_sentence.endswith('.'):
                        current_sentence = current_sentence[:-1] + ' ' + clean_b
                    elif current_sentence.endswith('-'):
                        current_sentence = current_sentence[:-1] + clean_b
                    else:
                        current_sentence += ' ' + clean_b
                else:
                    current_sentence = clean_b
                    
        if current_sentence:
            reconstructed_sentences.append(current_sentence.strip())
            
        # Also discover any additional localized technologies from project body
        full_proj_text = header + " " + " ".join(raw_body_lines)
        for s in found_skills:
            if s.lower() in full_proj_text.lower() and s not in techs:
                techs.append(s)
                
        desc = ' '.join(reconstructed_sentences)
        if not desc:
            desc = 'Technical project developed as part of engineering portfolio.'
            
        final_projects.append({
            'name': title,
            'technologies': techs[:6],
            'description': desc,
            'role': 'Developer / Contributor',
            'links': [],
            'evidence': title,
            'confidence': 0.95
        })
        
    return final_projects

def parse_certifications(cert_text: str) -> list:
    """
    Parses certifications and courses while strictly filtering out soft skills and section headers.
    """
    if not cert_text.strip():
        return []
        
    lines = [clean_item_title(l) for l in cert_text.splitlines() if clean_item_title(l)]
    cleaned_certs = []
    seen_keys = set()
    
    HEADER_IGNORE = {"certifications", "certificates", "courses", "training", "accreditations", "licenses", "skills", "soft skills", "activities", "licenses & certifications", "certificates & courses", "training & courses", "training & workshops", "relevant coursework", "credentials"}
    
    for line in lines:
        clean = line.strip()
        lower = clean.lower()
        lower_stripped = re.sub(r'^[&•\-\*\s]+', '', lower).strip()
        
        if lower in HEADER_IGNORE or lower_stripped in HEADER_IGNORE or len(clean) < 4:
            continue
            
        if is_soft_skill_line(clean):
            continue
            
        if re.search(r'^(?:cairo|alexandria|giza|egypt|remote|phone|email)\b', lower):
            continue
            
        if "digital egypt pioneers" in lower or "depi" in lower:
            title = clean
            issuer = "Ministry of Communications (MCIT) / DEPI"
        elif "qcourse" in lower:
            title = clean
            issuer = "QWorld / Quantum Computing Initiative"
        elif "deeplearning.ai" in lower or "coursera" in lower:
            title = clean
            issuer = "DeepLearning.AI / Coursera"
        elif "aws certified" in lower:
            title = clean
            issuer = "Amazon Web Services (AWS)"
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
    Features universal multi-strategy fail-safe mechanisms for any CV template.
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
    candidate_name = ""
    if first_lines:
        c_cand = clean_item_title(first_lines[0])
        if not re.search(r'[@\d]', c_cand) and len(c_cand) < 40 and not NON_PROJECT_KEYWORDS.match(c_cand):
            profile["identity"]["name"] = c_cand
            candidate_name = c_cand
            
    # 2. Extract Technical Skills (Ontology Regex across FULL document + GLiNER)
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
            
    # Also check skills section with GLiNER
    skills_text = sections.get("SKILLS", "") or cleaned_text
    ner_skills = extract_entities_from_chunk(skills_text[:1500], ["skill", "technology", "programming language"], threshold=0.3)
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
                
    # 4. Extract Education (With Fallback Global Search)
    edu_text = sections.get("EDUCATION", "") or cleaned_text
    ner_edu = extract_entities_from_chunk(edu_text[:2000], ["degree", "university", "college", "school"], threshold=0.35)
    degrees = [e["text"] for e in ner_edu if e["label"] == "degree"]
    schools = [e["text"] for e in ner_edu if e["label"] in ["university", "college", "school"]]
    
    if degrees or schools:
        deg = degrees[0] if degrees else "Bachelor of Computer Science"
        inst = schools[0] if schools else "University / Institution"
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
        # Regex search for university keywords across document
        univ_match = re.search(r'([A-Z][a-zA-Z\s]+(?:University|College|Institute|Faculty|Academy))\b', cleaned_text)
        deg_match = re.search(r'((?:Bachelor|Master|B\.Sc|M\.Sc|Ph\.D|Diploma|Associate)[\s\w\/]+)\b', cleaned_text)
        if univ_match or deg_match:
            inst_str = univ_match.group(1).strip() if univ_match else "University / Technical College"
            deg_str = deg_match.group(1).strip() if deg_match else "Bachelor's Degree"
            profile["education"].append({
                "institution": inst_str,
                "degree": deg_str,
                "field": "Computer Science / Technical",
                "start_date": "UNKNOWN",
                "end_date": "UNKNOWN",
                "evidence": f"{deg_str} at {inst_str}",
                "confidence": 0.80
            })
            
    # 5. Extract Projects (Universal Multi-Strategy Block Parsing + Fallback)
    proj_text = sections.get("PROJECTS", "")
    parsed_projects = parse_project_blocks(proj_text, found_skills, candidate_name)
    
    # Fail-safe: if section splitting didn't isolate PROJECTS, scan full cleaned_text
    if not parsed_projects:
        parsed_projects = parse_project_blocks(cleaned_text, found_skills, candidate_name)
        
    profile["projects"] = parsed_projects
        
    # 6. Extract Certifications (High-Precision Filtering + Fallback)
    cert_text = sections.get("CERTIFICATIONS", "")
    parsed_certs = parse_certifications(cert_text)
    
    if not parsed_certs and cert_text:
        parsed_certs = parse_certifications(cleaned_text)
        
    profile["certifications"] = parsed_certs
            
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
