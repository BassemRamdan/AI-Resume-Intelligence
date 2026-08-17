"""
Resume extraction compatibility wrapper.
Re-exports from lib.resume package.
"""

from .resume import (
    SKILL_ONTOLOGY,
    CRITICAL_SKILLS,
    normalize_skill,
    clean_text,
    split_into_sections,
    extract_pdf_layout,
    extract_resume
)

__all__ = [
    "SKILL_ONTOLOGY",
    "CRITICAL_SKILLS",
    "normalize_skill",
    "clean_text",
    "split_into_sections",
    "extract_pdf_layout",
    "extract_resume"
]
