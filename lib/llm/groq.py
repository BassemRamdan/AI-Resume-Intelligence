"""
Grounded Groq LLM Provider.
Generates natural language explanations using candidate JSON evidence.
Includes automatic fallback to deterministic explanations to prevent user-facing errors.
"""

import os
import json
from .prompts import get_prompt

def explain_career_fit(similarity_data: dict, api_key: str = None) -> dict:
    """
    Generates structured career fit explanation grounded in deterministic JSON evidence.
    """
    if api_key is None:
        api_key = os.environ.get("GROQ_API_KEY", "")
        
    primary_cat = similarity_data.get("classification", {}).get("category", "General")
    career_fits = similarity_data.get("career_fit", [])
    
    # Deterministic fallback builder
    def build_fallback():
        return {
            "classification_analysis": f"Primary classification signal indicates highest compatibility with {primary_cat}.",
            "top_careers": [
                {
                    "career": m.get("career", ""),
                    "total_fit": m.get("total_fit", 0),
                    "why": f"Evaluated with {m.get('total_fit', 0)}% fit based on verified skills ({', '.join(m.get('evidence', {}).get('matched_skills', [])[:4]) or 'core technical competencies'}), experience match, and domain similarity.",
                    "missing_evidence": f"Recommended growth in: {', '.join(m.get('evidence', {}).get('missing_skills', [])[:3])}." if m.get('evidence', {}).get('missing_skills') else "Strong alignment with core criteria."
                }
                for m in career_fits[:3]
            ],
            "similar_profiles_analysis": "Semantic similarity peer group calculated via KNN embeddings comparison."
        }

    if not api_key:
        return build_fallback()
        
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        system_instruction = get_prompt("explanation")
        user_content = f"""
{system_instruction}

RAW ENGINE DATA:
{json.dumps(similarity_data, indent=2)}

Return a strict JSON object following this exact schema:
{{
  "classification_analysis": "1 sentence explaining the primary classification.",
  "top_careers": [
    {{
      "career": "The exact career name (e.g. Machine Learning Engineer)",
      "total_fit": 0.0,
      "why": "A 2-3 sentence explanation connecting their matched skills and projects to this career.",
      "missing_evidence": "A 1 sentence explanation of what they are missing based on missing_skills array."
    }}
  ],
  "similar_profiles_analysis": "A 1-2 sentence summary explaining the KNN semantic similarity peer group."
}}
"""
        candidate_models = ["allam-2-7b", "qwen/qwen3.6-27b"]
        for model_id in candidate_models:
            try:
                res = client.chat.completions.create(
                    messages=[{"role": "user", "content": user_content}],
                    model=model_id,
                    response_format={"type": "json_object"},
                    temperature=0.2
                )
                raw_json = res.choices[0].message.content
                if raw_json:
                    return json.loads(raw_json)
            except Exception as e:
                print(f"Warning: Groq request with {model_id} failed: {e}")
                
        return build_fallback()
    except Exception as e:
        print(f"Warning: Groq explanation pipeline failed: {e}")
        return build_fallback()
