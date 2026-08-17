import { GroqProvider } from './lib/providers/GroqProvider';
import * as dotenv from 'dotenv';
dotenv.config({ path: '.env.local' });

async function run() {
  const g = new GroqProvider();
  
  const rawProfile = {
    "identity": {},
    "summary": "UNKNOWN",
    "skills": [
      {
        "name": "SQL",
        "normalized_name": "SQL",
        "category": "UNKNOWN",
        "evidence": "John Doe SKILLS Python, SQL, Java, React, Next.js EXPERIE",
        "confidence": 0.95
      }
    ],
    "education": [
      {
        "degree": "Bachelor of Computer Science",
        "institution": "MIT",
        "evidence": "Bachelor of Computer Science from MIT",
        "confidence": 0.8
      }
    ],
    "experience": [
      {
        "job_title": "Software Engineer",
        "company": "Google",
        "evidence": "Software Engineer at Google\nDeveloped APIs.",
        "confidence": 0.8
      }
    ],
    "projects": [
      {
        "title": "CareerLens",
        "description": "UNKNOWN",
        "technologies": [
          "AI",
          "CareerLens"
        ],
        "evidence": "CareerLens AI\nBuilt an AI resume parser.",
        "confidence": 0.8
      }
    ],
    "certifications": [
      {
        "name": "AWS Certified Solutions Architect",
        "issuer": "Various",
        "evidence": "AWS Certified Solutions Architect",
        "confidence": 0.8
      }
    ],
    "languages": [],
    "achievements": [],
    "layout_features": {
      "has_columns": false,
      "font_hierarchy_levels": 1,
      "total_blocks": 13
    },
    "career_signal": {
      "dataset_category": "INFORMATION-TECHNOLOGY",
      "confidence": 0.5534466505050659
    },
    "filename": "dummy_resume.pdf",
    "raw_text_snippet": "John Doe\nSKILLS\nPython, SQL, Java, React, Next.js\nEXPERIENCE\nSoftware Engineer at Google\nDeveloped APIs.\nPROJECTS\nCareerLens AI\nBuilt an AI resume parser.\nEDUCATION\nBachelor of Computer Science from MIT\nCERTIFICATIONS\nAWS Certified Solutions Architect"
  };

  const res = await g.cleanProfile(rawProfile);
  console.log(JSON.stringify(res, null, 2));
}

run().catch(console.error);
