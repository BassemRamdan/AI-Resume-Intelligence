"""
AI Career Advisor Chatbot Service.
Integrates Groq API with deterministic career roadmap fallback
to provide interactive career counseling, skill gap identification, and milestone planning.
"""

import os
import json
import requests
from .prompts import get_prompt
from ..career.taxonomy import CAREER_TAXONOMY, get_career_roadmap

GROQ_MODELS = [
    "allam-2-7b",
    "qwen/qwen3.6-27b",
    "llama-3.1-8b-instant"
]

def generate_deterministic_advice(user_query: str, candidate_profile: dict, target_career: str = None) -> str:
    """Generates a structured, evidence-backed roadmap and advice when LLM is unreachable."""
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
    req_skills = tax_info["skills"]
    matched = [s for s in skills if any(s.lower() == r.lower() for r in req_skills)]
    missing = [r for r in req_skills if not any(r.lower() == s.lower() for s in skills)]
    roadmap = get_career_roadmap(target_career)
    
    # Detect language (Arabic vs English)
    is_arabic = any(ord(c) >= 0x0600 and ord(c) <= 0x06FF for c in user_query)
    
    if is_arabic:
        response = f"""### 🎯 خطة التطوير المهني المخصصة لمسار: **{target_career}**

---

#### 🌟 1. نقاط القوة الحالية في سيرتك الذاتية:
- **المهارات المتطابقة:** {', '.join(matched) if matched else 'لم يتم رصد مهارات مباشرة بعد'}
- **المشاريع المسجلة:** {', '.join(projects) if projects else 'لا توجد مشاريع مضافة'}

---

#### 🔍 2. الفجوة المهارية وما ينقصك للتميز:
- **المهارات والتقنيات المستهدفة:** {', '.join(missing[:5])}

---

#### 🗺️ 3. خارطة الطريق المقترحة (Step-by-Step Roadmap):
- **المرحلة الأولى (الأساسيات):** {roadmap.get('phase_1', '')}
- **المرحلة الثانية (التطبيق والمشاريع):** {roadmap.get('phase_2', '')}
- **المرحلة الثالثة (الاحتراف والإنتاج):** {roadmap.get('phase_3', '')}

---

#### 💡 نصيحة مهنية:
قم ببناء مشروع متكامل يدمج المهارات الناقصة ({', '.join(missing[:3])}) وارفعه على GitHub مع توثيق احترافي (README) لتعزيز فرص قبولك.
"""
    else:
        response = f"""### 🎯 Personalized Career Growth Roadmap: **{target_career}**

---

#### 🌟 1. Current Verified Strengths:
- **Matched Skills:** {', '.join(matched) if matched else 'None directly detected yet'}
- **Existing Projects:** {', '.join(projects) if projects else 'No projects registered'}

---

#### 🔍 2. Skill Gap Analysis:
- **High-Priority Missing Skills:** {', '.join(missing[:5])}

---

#### 🗺️ 3. Actionable Milestone Roadmap:
- **Phase 1 (Foundations):** {roadmap.get('phase_1', '')}
- **Phase 2 (Hands-On Projects & Tooling):** {roadmap.get('phase_2', '')}
- **Phase 3 (Production Mastery & Leadership):** {roadmap.get('phase_3', '')}

---

#### 💡 Pro Tip:
Develop an end-to-end portfolio project incorporating your target skills ({', '.join(missing[:3])}) and document system architecture on GitHub to maximize recruiter impact.
"""
    return response

def chat_career_advisor(messages: list, candidate_profile: dict = None, target_career: str = None) -> str:
    """
    Coordinates chat session with the AI Career Advisor.
    Utilizes candidate profile, target career taxonomy, and Groq API with robust fallback.
    """
    if not candidate_profile:
        candidate_profile = {}
        
    last_user_message = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            last_user_message = m.get("content", "")
            break
            
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return generate_deterministic_advice(last_user_message, candidate_profile, target_career)
        
    sys_prompt = get_prompt("chatbot")
    
    # Build context
    skills_str = ", ".join([s.get("name", "") for s in candidate_profile.get("skills", [])])
    projects_str = ", ".join([p.get("name", "") for p in candidate_profile.get("projects", [])])
    
    target_info = CAREER_TAXONOMY.get(target_career, {}) if target_career else {}
    req_skills = ", ".join(target_info.get("skills", []))
    roadmap_info = json.dumps(get_career_roadmap(target_career) if target_career else {})
    
    context_str = f"""
Candidate Verified Profile:
- Skills: {skills_str}
- Projects: {projects_str}
- Target Track: {target_career or 'General Career Advisory'}
- Target Standard Skills: {req_skills}
- Reference Roadmap: {roadmap_info}
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
                    "temperature": 0.4,
                    "max_tokens": 1000
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
