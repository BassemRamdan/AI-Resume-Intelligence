"""
AI Career Advisor Chatbot Service.
Equipped with dense semantic RAG over the Career Roadmaps Knowledge Base.
Integrates Groq API with deterministic English fallback.
"""

import os
import json
import requests
from .prompts import get_prompt
from ..career.taxonomy import CAREER_TAXONOMY, get_career_roadmap
from ..career.rag import retrieve_roadmap_context

GROQ_MODELS = [
    "allam-2-7b",
    "qwen/qwen3.6-27b",
    "llama-3.1-8b-instant"
]

def generate_deterministic_advice(user_query: str, candidate_profile: dict, target_career: str = None) -> str:
    """Generates a structured, evidence-backed English roadmap and advice when LLM is unreachable."""
    skills = [s.get("name", "") for s in candidate_profile.get("skills", [])]
    projects = [p.get("name", "") for p in candidate_profile.get("projects", [])]
    
    # Determine target career
    if not target_career:
        target_career = "Software Engineer"
        for c_name in CAREER_TAXONOMY.keys():
            if any(s.lower() in [x.lower() for x in CAREER_TAXONOMY[c_name]["skills"]] for s in skills):
                target_career = c_name
                break
                
    tax_info = CAREER_TAXONOMY.get(target_career, CAREER_TAXONOMY["Software Engineer"])
    req_skills = tax_info.get("skills", [])
    matched = [s for s in skills if any(s.lower() == r.lower() for r in req_skills)]
    missing = [r for r in req_skills if not any(r.lower() == s.lower() for s in skills)]
    roadmap = get_career_roadmap(target_career)
    
    response = f"""### 🎯 Personalized Career Growth Roadmap: **{target_career}**

---

#### 🌟 1. Verified Profile Strengths
- **Matched Skills:** {', '.join(matched) if matched else 'None directly detected in current profile'}
- **Existing Projects:** {', '.join(projects) if projects else 'No portfolio projects registered yet'}

---

#### 🔍 2. High-Priority Skill Gap Analysis
The following critical competencies are required to reach full competitiveness in the **{target_career}** track:
{chr(10).join([f"- **{s}**: High-demand standard requirement." for s in missing[:5]])}

---

#### 🗺️ 3. Step-by-Step Milestone Roadmap
- **Phase 1 (Foundations & Core Prerequisites):**
  {roadmap.get('phase_1', 'Master fundamental theoretical concepts, language syntax, and development workflows.')}
  - [ ] Study core theoretical concepts and underlying system mechanics.
  - [ ] Solidify version control and clean coding patterns.

- **Phase 2 (Applied Engineering & Must-Build Portfolio Projects):**
  {roadmap.get('phase_2', 'Build production-ready deliverables and implement end-to-end architectural patterns.')}
  - [ ] Build a production-grade deliverable implementing missing skills ({', '.join(missing[:3]) if missing else 'Core Architecture'}).
  - [ ] Write automated unit/integration test suites and containerize with Docker.

- **Phase 3 (Production Mastery, System Design & Leadership):**
  {roadmap.get('phase_3', 'Master distributed architectures, cloud scalability, and cross-functional leadership.')}
  - [ ] Complete system design assessments and high-throughput optimization.
  - [ ] Deploy to cloud infrastructure with CI/CD and monitoring.

---

#### 💡 Actionable Engineering Pro-Tip
Build an end-to-end portfolio project addressing your missing skills (**{', '.join(missing[:3]) if missing else 'Advanced Architecture'}**) with full documentation, architectural diagrams, and test suites on GitHub to significantly increase recruiter engagement.
"""
    return response

def chat_career_advisor(messages: list, candidate_profile: dict = None, target_career: str = None) -> str:
    """
    Coordinates chat session with the AI Career Advisor.
    Enforces English-only output and augments LLM context with dense semantic RAG chunks.
    """
    if not candidate_profile:
        candidate_profile = {}
        
    last_user_message = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user_message = m.get("content", "")
            break
            
    # Retrieve top-k semantic RAG chunks from Career Roadmaps Knowledge Base
    rag_context = retrieve_roadmap_context(last_user_message, target_career=target_career, top_k=3)
    
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return generate_deterministic_advice(last_user_message, candidate_profile, target_career)
        
    sys_prompt = get_prompt("chatbot")
    
    # Build candidate evidence context
    skills_str = ", ".join([s.get("name", "") for s in candidate_profile.get("skills", [])])
    projects_str = ", ".join([p.get("name", "") for p in candidate_profile.get("projects", [])])
    
    target_info = CAREER_TAXONOMY.get(target_career, {}) if target_career else {}
    req_skills = ", ".join(target_info.get("skills", []))
    
    context_str = f"""
CANDIDATE EVIDENCE PROFILE:
- Extracted Skills: {skills_str or 'None detected'}
- Extracted Projects: {projects_str or 'None detected'}
- Target Career Track: {target_career or 'Software Engineer'}
- Target Baseline Skills: {req_skills}

RETRIEVED EXPERT RAG KNOWLEDGE BASE CHUNKS (Reference Roadmap, Project Blueprints & Senior Milestones):
{rag_context}
"""
    
    full_messages = [
        {"role": "system", "content": f"{sys_prompt}\n\n{context_str}"}
    ]
    
    for m in messages[-6:]:
        full_messages.append({"role": m.get("role", "user"), "content": m.get("content", "")})
        
    for model_name in GROQ_MODELS:
        try:
            res = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model_name,
                    "messages": full_messages,
                    "temperature": 0.3,
                    "max_tokens": 1200
                },
                timeout=12
            )
            if res.status_code == 200:
                data = res.json()
                content = data["choices"][0]["message"]["content"]
                if content and len(content.strip()) > 10:
                    return content
        except Exception as e:
            print(f"Chatbot model {model_name} error: {e}")
            continue
            
    return generate_deterministic_advice(last_user_message, candidate_profile, target_career)
