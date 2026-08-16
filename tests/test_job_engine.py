import sys
import os
import unittest

# Ensure we can import lib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.ai.job_engine import JobEngine, MatchingEngine

class TestJobEngine(unittest.TestCase):
    def setUp(self):
        self.engine = JobEngine()
        self.matcher = MatchingEngine(self.engine)

    def test_url_validation_accepts_valid(self):
        self.assertTrue(self.engine.is_valid_url("https://www.google.com/jobs/123"))
        self.assertTrue(self.engine.is_valid_url("http://adzuna.com/search"))
        
    def test_url_validation_rejects_invalid(self):
        self.assertFalse(self.engine.is_valid_url(""))
        self.assertFalse(self.engine.is_valid_url("UNKNOWN"))
        self.assertFalse(self.engine.is_valid_url("javascript:alert(1)"))
        self.assertFalse(self.engine.is_valid_url("https://localhost:3000/job/1"))
        self.assertFalse(self.engine.is_valid_url("http://127.0.0.1:8000/api"))
        self.assertFalse(self.engine.is_valid_url("https://demo.corp/jobs/1"))

    def test_deduplication(self):
        jobs = [
            {"title": "Dev", "company": "A", "location": "NY", "url": "https://a.com/1", "source": "Adzuna", "sourceJobId": "1"},
            {"title": "Dev", "company": "A", "location": "NY", "url": "https://a.com/1", "source": "Adzuna", "sourceJobId": "1"}, # Exact dup
            {"title": "Dev", "company": "A", "location": "NY", "url": "https://a.com/2", "source": "LinkedIn", "sourceJobId": "2"} # Dup by hash
        ]
        unique = self.engine.remove_duplicates(jobs)
        self.assertEqual(len(unique), 1)
        self.assertEqual(unique[0]["sourceJobId"], "1")

    def test_skill_extraction_and_normalization(self):
        job = {
            "title": "Data Scientist",
            "description": "Looking for python, pytorch, and machine learning experts."
        }
        processed = self.engine.extract_information(job)
        skills = processed["required_skills"]
        # Assuming ontology maps "python" -> "Python"
        # It's an unordered set converted to list
        skills_set = set(skills)
        self.assertTrue("Python" in skills_set)
        self.assertTrue("PyTorch" in skills_set)
        self.assertTrue("Machine Learning" in skills_set)
        
    def test_deterministic_matching(self):
        job = {
            "required_skills": ["Python", "PyTorch", "Docker"]
        }
        profile = {
            "skills": ["Python", "PyTorch", "React"]
        }
        
        result = self.matcher.match(job, profile)
        
        self.assertEqual(len(result["matched_skills"]), 2)
        self.assertEqual(len(result["missing_required_skills"]), 1)
        self.assertTrue("Docker" in result["missing_required_skills"])
        
        # 2 out of 3 = 66.6%
        self.assertAlmostEqual(result["overall_match_score"], 66.7, places=1)

if __name__ == "__main__":
    unittest.main()
