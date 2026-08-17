"""
Skill ontology compatibility wrapper.
Re-exports from lib.resume.ontology.
"""

from .resume.ontology import SKILL_ONTOLOGY, CRITICAL_SKILLS, normalize_skill

__all__ = ["SKILL_ONTOLOGY", "CRITICAL_SKILLS", "normalize_skill"]
