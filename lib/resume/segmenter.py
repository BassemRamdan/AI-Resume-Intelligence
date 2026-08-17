"""
Heuristic Section Segmentation Module.
Segments cleaned resume text into functional blocks: SKILLS, EXPERIENCE, EDUCATION, PROJECTS, CERTIFICATIONS.
"""

import re

SECTION_PATTERNS = {
    "SKILLS": r'(?:^|\n)(?:\d+\.\s*)?(?:technical\s+|core\s+)?(?:skills|technologies|proficiencies|tech\s+stack|competencies|expertise|tools\s+&\s+technologies)\b[:\s]*',
    "EXPERIENCE": r'(?:^|\n)(?:\d+\.\s*)?(?:work\s+|professional\s+|employment\s+)?(?:experience|history|employment|work\s+history|career\s+history)\b[:\s]*',
    "EDUCATION": r'(?:^|\n)(?:\d+\.\s*)?(?:education|academic\s+background|qualifications|academic\s+history)\b[:\s]*',
    "PROJECTS": r'(?:^|\n)(?:\d+\.\s*)?(?:key\s+|technical\s+|academic\s+|personal\s+)?(?:projects|portfolio|open\s+source|work\s+samples)\b[:\s]*',
    "CERTIFICATIONS": r'(?:^|\n)(?:\d+\.\s*)?(?:certifications|certificates|licenses|courses|accreditations)\b[:\s]*'
}

def clean_text(text: str) -> str:
    """Clean raw extracted PDF text from null characters and excessive whitespace."""
    if not text:
        return ""
    text = text.replace('\x00', '')
    text = re.sub(r'[\r\f\v]', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def split_into_sections(text: str) -> dict:
    """
    Identifies major resume sections using regularized heading anchors.
    Returns a dictionary mapping section names to their extracted text content.
    """
    cleaned = clean_text(text)
    positions = []
    
    for section_name, pattern in SECTION_PATTERNS.items():
        matches = list(re.finditer(pattern, cleaned, re.IGNORECASE))
        for m in matches:
            positions.append((m.start(), m.end(), section_name))
            
    # Sort detected headers by character offset
    positions = sorted(positions, key=lambda x: x[0])
    
    sections = {k: "" for k in SECTION_PATTERNS.keys()}
    sections["UNCLASSIFIED"] = ""
    
    if not positions:
        # Fallback: if no formal headers detected, treat whole text as unclassified
        sections["UNCLASSIFIED"] = cleaned
        sections["SKILLS"] = cleaned
        sections["EXPERIENCE"] = cleaned
        sections["EDUCATION"] = cleaned
        sections["PROJECTS"] = cleaned
        return sections
        
    # Text before first header
    first_pos = positions[0][0]
    if first_pos > 0:
        sections["UNCLASSIFIED"] = cleaned[:first_pos].strip()
        
    for i in range(len(positions)):
        _, start_content, sec_name = positions[i]
        end_content = positions[i+1][0] if i + 1 < len(positions) else len(cleaned)
        content = cleaned[start_content:end_content].strip()
        
        if sections[sec_name]:
            sections[sec_name] += "\n\n" + content
        else:
            sections[sec_name] = content
            
    return sections
