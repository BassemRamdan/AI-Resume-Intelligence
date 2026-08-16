import sys
import json
import re
import warnings
import os

# Add current directory to path so we can import skill_ontology
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from skill_ontology import normalize_skill, CRITICAL_SKILLS, SKILL_ONTOLOGY
except ImportError:
    # Fallback if running from weird context
    def normalize_skill(x): return x.strip()
    CRITICAL_SKILLS = set()
    SKILL_ONTOLOGY = {}

# Suppress warnings for cleaner JSON output
warnings.filterwarnings("ignore")

try:
    from pypdf import PdfReader
    import fitz # PyMuPDF for Computer Vision layout analysis
    import torch
    from gliner import GLiNER
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
except ImportError as e:
    print(json.dumps({"error": f"Missing dependency: {str(e)}. Please run pip install pypdf gliner transformers torch"}))
    sys.exit(1)

def clean_text(text):
    """Clean basic whitespace while preserving some line breaks for sectioning."""
    clean = re.sub(r'[\r\n]+', '\n', text)
    clean = re.sub(r'[^\w\s.,;:\-@/\n]', '', clean)
    return clean.strip()

def split_into_sections(text):
    """Robust heuristic-based section splitting."""
    section_headers = {
        "SUMMARY": [r"\bsummary\b", r"\bprofile\b", r"\bobjective\b", r"\babout me\b", r"\bprofessional summary\b"],
        "EXPERIENCE": [r"\bexperience\b", r"\bwork experience\b", r"\bemployment\b", r"\bprofessional experience\b", r"\bwork history\b", r"\bcareer history\b"],
        "PROJECTS": [r"\bprojects\b", r"\bpersonal projects\b", r"\bacademic projects\b", r"\bopen source\b", r"\bportfolio\b"],
        "EDUCATION": [r"\beducation\b", r"\bacademic background\b", r"\bacademic history\b", r"\bqualifications\b"],
        "CERTIFICATIONS": [r"\bcertifications\b", r"\blicenses\b", r"\btraining\b", r"\bcourses\b"],
        "SKILLS": [r"\bskills\b", r"\btechnical skills\b", r"\bcore competencies\b", r"\btechnologies\b", r"\bexpertise\b"],
        "ACHIEVEMENTS": [r"\bachievements\b", r"\bawards\b", r"\bhonors\b"]
    }
    
    sections = {}
    current_section = "UNCLASSIFIED"
    sections[current_section] = []
    
    lines = text.split('\n')
    for line in lines:
        cleaned_line = line.strip().lower()
        if not cleaned_line:
            continue
            
        is_header = False
        # A line is likely a header if it is short (<= 5 words) and matches a keyword regex
        word_count = len(cleaned_line.split())
        if word_count <= 5:
            for sec_name, regex_list in section_headers.items():
                if any(re.search(pat, cleaned_line) for pat in regex_list):
                    current_section = sec_name
                    if current_section not in sections:
                        sections[current_section] = []
                    is_header = True
                    break
                    
        if not is_header:
            sections[current_section].append(line.strip())
            
    return {k: "\n".join(v) for k, v in sections.items()}

def extract_resume(filepath):
    # 1. Computer Vision / Layout Analysis & Text Extraction
    layout_features = {
        "has_columns": False,
        "font_hierarchy_levels": 1,
        "total_blocks": 0
    }
    text = ""
    
    try:
        # Try CV approach first with PyMuPDF
        doc = fitz.open(filepath)
        fonts = set()
        blocks_count = 0
        x0_positions = set()
        
        for page in doc:
            text += page.get_text() + "\n"
            dict_data = page.get_text("dict")
            for block in dict_data.get("blocks", []):
                if block.get("type") == 0: # Text block
                    blocks_count += 1
                    bbox = block.get("bbox", [])
                    if len(bbox) == 4:
                        # simple column detection heuristic based on X positions
                        x0 = round(bbox[0] / 50.0) * 50
                        x0_positions.add(x0)
                        
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            fonts.add(round(span.get("size", 10), 1))
                            
        layout_features["total_blocks"] = blocks_count
        layout_features["font_hierarchy_levels"] = len(fonts)
        layout_features["has_columns"] = len(x0_positions) > 2
        
    except Exception:
        # Fallback to simple text extraction if PyMuPDF CV fails
        try:
            reader = PdfReader(filepath)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            print(json.dumps({"error": f"Failed to read PDF: {str(e)}"}))
            return

    cleaned_text = clean_text(text)
    sections = split_into_sections(cleaned_text)

    # 2. Extract Entities via GLiNER selectively
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    try:
        gliner_model = GLiNER.from_pretrained("urchade/gliner_multi-v2.1").to(device)
    except Exception as e:
        print(json.dumps({"error": f"GLiNER loading failed: {str(e)}"}))
        return

    # Helper function for targeted extraction
    def extract_from_text(text_chunk, labels, threshold=0.4):
        if not text_chunk.strip():
            return []
        # Chunk if too long for GLiNER
        max_chars = 1500
        chunks = [text_chunk[i:i+max_chars] for i in range(0, len(text_chunk), max_chars)]
        results = []
        for chunk in chunks:
            preds = gliner_model.predict_entities(chunk, labels, threshold=threshold)
            results.extend(preds)
        return results

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
        "career_signal": {"dataset_category": "UNKNOWN_CATEGORY", "confidence": 0.0}
    }
    
    # 3. Process Sections
    
    # --- SKILLS ---
    found_skills = set()
    skill_evidence = {}
    
    # Regex fallback across ENTIRE text
    text_lower = cleaned_text.lower()
    for raw_skill, canonical in SKILL_ONTOLOGY.items():
        pattern = r'\b' + re.escape(raw_skill) + r'\b'
        match = re.search(pattern, text_lower)
        if match:
            found_skills.add(canonical)
            # Find a short snippet for evidence
            start = max(0, match.start() - 30)
            end = min(len(text_lower), match.end() + 30)
            skill_evidence[canonical] = cleaned_text[start:end].replace('\n', ' ').strip()
            
    # GLiNER on Skills and Unclassified
    skill_text = sections.get("SKILLS", "") + "\n" + sections.get("UNCLASSIFIED", "")
    if skill_text.strip():
        preds = extract_from_text(skill_text, ["skill"], threshold=0.3)
        for p in preds:
            norm = normalize_skill(p["text"])
            if norm not in found_skills:
                found_skills.add(norm)
                skill_evidence[norm] = p["text"]
                
    for s in found_skills:
        profile["skills"].append({
            "name": s,
            "normalized_name": s,
            "category": "UNKNOWN",
            "evidence": skill_evidence.get(s, "Detected via regex"),
            "confidence": 0.95
        })
        
    if not profile["skills"]:
        profile["skills"] = [{"name": "UNKNOWN", "evidence": "NOT_FOUND", "confidence": 0.0}]

    # --- EXPERIENCE ---
    exp_text = sections.get("EXPERIENCE", "")
    if exp_text:
        preds = extract_from_text(exp_text, ["job title", "company", "date"], threshold=0.2)
        
        current_job = {"job_title": "UNKNOWN", "company": "UNKNOWN", "evidence": "", "confidence": 0.8}
        
        for p in preds:
            if p["label"] == "job title":
                current_job["job_title"] = p["text"]
            elif p["label"] == "company":
                current_job["company"] = p["text"]
                
        # Dump up to 3000 chars of the block so Groq can fully reconstruct all jobs
        current_job["evidence"] = exp_text[:3000] 
        profile["experience"].append(current_job)
            
    if not profile["experience"]:
        profile["experience"] = [{"job_title": "UNKNOWN", "company": "UNKNOWN", "evidence": "NOT_FOUND", "confidence": 0.0}]

    # --- PROJECTS ---
    proj_text = sections.get("PROJECTS", "")
    if proj_text:
        preds = extract_from_text(proj_text, ["project name"], threshold=0.2)
        project_names = [p["text"] for p in preds if p["label"] == "project name"]
        
        if project_names:
            # Keep order and make unique
            seen = set()
            unique_names = []
            for name in project_names:
                if name.lower() not in seen:
                    unique_names.append(name)
                    seen.add(name.lower())
            
            for i, name in enumerate(unique_names):
                idx = proj_text.find(name)
                start_idx = max(0, idx - 50) if idx != -1 else 0
                
                # Next project start or end of text
                if i + 1 < len(unique_names):
                    next_idx = proj_text.find(unique_names[i+1])
                    end_idx = next_idx if next_idx != -1 and next_idx > start_idx else len(proj_text)
                else:
                    end_idx = len(proj_text)
                    
                chunk = proj_text[start_idx:end_idx].strip()
                
                # Extract technologies specific to this project chunk
                tech_preds = extract_from_text(chunk, ["technology", "programming language", "framework"], threshold=0.2)
                techs = list(set([t["text"] for t in tech_preds]))
                
                profile["projects"].append({
                    "title": name,
                    "description": "UNKNOWN",
                    "technologies": techs if techs else ["UNKNOWN"],
                    "evidence": chunk[:1500],
                    "confidence": 0.8
                })
        else:
            # Fallback if GLiNER misses project names but section exists
            profile["projects"].append({
                "title": "General Projects",
                "description": "UNKNOWN",
                "technologies": ["UNKNOWN"],
                "evidence": proj_text[:2000],
                "confidence": 0.5
            })
            
    if not profile["projects"]:
        profile["projects"] = []

    # --- EDUCATION ---
    edu_text = sections.get("EDUCATION", "")
    if edu_text:
        preds = extract_from_text(edu_text, ["degree", "university"], threshold=0.4)
        edu = {"degree": "UNKNOWN", "institution": "UNKNOWN", "evidence": edu_text[:500], "confidence": 0.8}
        
        for p in preds:
            if p["label"] == "degree" and p["text"].lower() not in ["bachelor", "master", "university"]:
                edu["degree"] = p["text"]
            elif p["label"] == "university":
                edu["institution"] = p["text"]
                
        if edu["degree"] != "UNKNOWN" or edu["institution"] != "UNKNOWN":
            profile["education"].append(edu)
            
    if not profile["education"]:
        profile["education"] = [{"institution": "UNKNOWN", "degree": "UNKNOWN", "evidence": "NOT_FOUND", "confidence": 0.0}]

    # --- CERTIFICATIONS ---
    cert_text = sections.get("CERTIFICATIONS", "")
    if cert_text:
        preds = extract_from_text(cert_text, ["certification"], threshold=0.4)
        for p in preds:
            # Filter generic headers
            if p["text"].lower() not in ["certifications", "training certifications", "courses"]:
                profile["certifications"].append({
                    "name": p["text"],
                    "issuer": "UNKNOWN",
                    "evidence": cert_text[:500],
                    "confidence": 0.8
                })
                
    if not profile["certifications"]:
        profile["certifications"] = [{"name": "UNKNOWN", "evidence": "NOT_FOUND", "confidence": 0.0}]

    # 4. Classify via DeBERTa
    predicted_category = "INFORMATION-TECHNOLOGY" # default fallback
    try:
        model_name = "BassemRamdan/resume-classifier-deberta"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        classifier = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
    except Exception as e:
        classifier = None

    if classifier:
        inputs = tokenizer(cleaned_text, padding=True, truncation=True, max_length=512, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = classifier(**inputs)
            logits = outputs.logits
            predicted_idx = torch.argmax(logits, dim=-1).item()
            
        predicted_category = classifier.config.id2label.get(predicted_idx, "UNKNOWN_CATEGORY")
        
    profile["career_signal"]["dataset_category"] = predicted_category
    profile["career_signal"]["confidence"] = 0.9

    # Add system fields
    profile["filename"] = filepath.split("/")[-1].split("\\")[-1]
    profile["raw_text_snippet"] = cleaned_text[:3000] # Provide extensive raw text for Groq validation

    # Must only print JSON to stdout so Node.js can parse it
    print("===START===")
    print(json.dumps(profile))
    print("===END===")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("===START===")
        print(json.dumps({"error": "No file path provided"}))
        print("===END===")
        sys.exit(1)
    
    filepath = sys.argv[1]
    extract_resume(filepath)
