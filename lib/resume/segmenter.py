"""
Heuristic Section Segmentation Module.
Segments cleaned resume text into functional blocks:
SKILLS, SOFT_SKILLS, EXPERIENCE, EDUCATION, PROJECTS, CERTIFICATIONS, LANGUAGES, ACTIVITIES, SUMMARY.
Features prioritized multi-word heading patterns.
"""

import re

SECTION_PATTERNS = {
    "SUMMARY": r'(?:^|\n)(?:\d+\.\s*)?(?:professional\s+summary|executive\s+summary|career\s+objective|about\s+me|summary|profile|objective)\b[:\s]*',
    "SKILLS": r'(?:^|\n)(?:\d+\.\s*)?(?:technical\s+proficiencies|technical\s+expertise|tools\s+&\s+technologies|programming\s+languages|languages\s+&\s+frameworks|areas\s+of\s+expertise|technical\s+skills|core\s+competencies|key\s+skills|tech\s+stack|proficiencies|technologies|competencies|expertise|toolkit|skills|tools)\b[:\s]*',
    "SOFT_SKILLS": r'(?:^|\n)(?:\d+\.\s*)?(?:interpersonal\s+skills|personal\s+traits|soft\s+skills|competencies|qualities|attributes)\b[:\s]*',
    "EXPERIENCE": r'(?:^|\n)(?:\d+\.\s*)?(?:professional\s+experience|employment\s+history|career\s+history|work\s+experience|relevant\s+experience|industry\s+experience|work\s+history|experience|employment|internships|background)\b[:\s]*',
    "EDUCATION": r'(?:^|\n)(?:\d+\.\s*)?(?:academic\s+qualifications|academic\s+background|education\s+&\s+training|academic\s+history|academic\s+record|qualifications|education|degrees)\b[:\s]*',
    "PROJECTS": r'(?:^|\n)(?:\d+\.\s*)?(?:portfolio\s+&\s+production\s+projects|portfolio\s+&\s+projects|technical\s+projects|practical\s+projects|academic\s+projects|personal\s+projects|selected\s+projects|featured\s+projects|software\s+projects|key\s+projects|project\s+experience|open\s+source|work\s+samples|portfolio|projects)\b[:\s]*',
    "CERTIFICATIONS": r'(?:^|\n)(?:\d+\.\s*)?(?:licenses\s*&\s*certifications|certificates\s*&\s*courses|certificates\s*&\s*training|professional\s+certifications|licenses\s*&\s*credentials|training\s*&\s*courses|certifications|certificates|licenses|accreditations|credentials)\b[:\s]*',
    "COURSES": r'(?:^|\n)(?:\d+\.\s*)?(?:relevant\s+coursework|training\s*&\s*workshops|courses|training|workshops|bootcamps|coursework)\b[:\s]*',
    "LANGUAGES": r'(?:^|\n)(?:\d+\.\s*)?(?:language\s+proficiency|language\s+skills|languages)\b[:\s]*',
    "ACTIVITIES": r'(?:^|\n)(?:\d+\.\s*)?(?:extracurricular\s+activities|volunteering\s+&\s+leadership|honors\s*&\s*awards|activities|extracurricular|volunteering|community|honors|awards|achievements|leadership)\b[:\s]*',
    "CONTACT": r'(?:^|\n)(?:\d+\.\s*)?(?:contact\s+information|personal\s+details|personal\s+info|contact\s+info|contact|location)\b[:\s]*'
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
        sections["UNCLASSIFIED"] = cleaned
        sections["SKILLS"] = cleaned
        sections["EXPERIENCE"] = cleaned
        sections["EDUCATION"] = cleaned
        sections["PROJECTS"] = cleaned
        sections["CERTIFICATIONS"] = cleaned
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
            
    # Merge COURSES into CERTIFICATIONS if found
    if sections.get("COURSES"):
        if sections.get("CERTIFICATIONS"):
            sections["CERTIFICATIONS"] += "\n\n" + sections["COURSES"]
        else:
            sections["CERTIFICATIONS"] = sections["COURSES"]
            
    return sections
