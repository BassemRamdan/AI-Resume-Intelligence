"""
AI Career Advisor Chatbot Service.
Equipped with dense semantic RAG over the Career Roadmaps Knowledge Base.
Powered by Groq 120B Flagship Model with dynamic conversational intelligence.
"""

import os
import re
import json
import requests
from dotenv import load_dotenv

# Ensure local environment variables are loaded
load_dotenv(".env.local")
load_dotenv(".env")

from .prompts import get_prompt
from ..career.taxonomy import CAREER_TAXONOMY, get_career_roadmap
from ..career.rag import retrieve_roadmap_context

GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "allam-2-7b",
    "qwen/qwen3.6-27b"
]

def generate_deterministic_advice(user_query: str, candidate_profile: dict, target_career: str = None) -> str:
    """Generates an intelligent, evidence-backed English technical response when LLM API is unreachable."""
    query_lower = user_query.lower()
    skills = [s.get("name", "") for s in candidate_profile.get("skills", [])]
    projects = [p.get("name", "") for p in candidate_profile.get("projects", [])]
    
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
    
    # Specific concept breakdowns
    if "python" in query_lower:
        return f"""### 🐍 Mastering Python for {target_career}

**Python** is the industry standard for backend development, data engineering, and machine learning.

---

#### 🗺️ Recommended Learning Roadmap:
1. **Core Foundations (Weeks 1-3):** Syntax, Data Structures (Lists, Dicts, Sets), OOP, Generators, Context Managers.
2. **Modern Tooling & Frameworks (Weeks 4-6):** FastAPI, AsyncIO, Type Hints (Pydantic), SQLAlchemy / Tortoise ORM.
3. **Applied Production Project (Weeks 7-9):** Build a high-throughput REST API with automated unit testing (PyTest) and Docker containerization.
4. **Cloud & Deployment (Weeks 10-12):** Deploy to AWS/Azure with CI/CD and Redis caching.

---

#### 💡 Integration with Your Profile:
Your profile demonstrates existing strengths in **{', '.join(skills[:3]) if skills else 'Software Engineering'}**. Learning Python will allow you to build cross-stack microservices and AI-driven APIs.
"""

    if "c#" in query_lower or "csharp" in query_lower:
        return f"""### 🔷 Mastering C# & .NET Core for {target_career}

**C# and .NET** power enterprise architectures, high-performance backends, cloud microservices, and distributed systems.

---

#### 🗺️ Recommended Learning Path:
1. **Language Mastery (Weeks 1-3):** Modern C# 12 features, LINQ, Generics, Async/Await, Memory Management (Garbage Collection & Structs).
2. **Enterprise Architecture (Weeks 4-6):** ASP.NET Core Web APIs, Entity Framework Core, Clean Architecture / CQRS with MediatR.
3. **Distributed Systems & Real-Time (Weeks 7-9):** SignalR WebSockets, Redis distributed caching, RabbitMQ message queues.
4. **Production Readiness (Weeks 10-12):** xUnit testing, Docker multi-stage builds, Azure DevOps CI/CD.

---

#### 💡 Profile Synergy:
Your profile already shows familiarity with **{', '.join(skills) if skills else 'Modern Technologies'}**. Double down on Clean Architecture and Microservices to qualify for Senior .NET Engineer roles.
"""

    if "docker" in query_lower:
        return """### 🐳 Understanding Docker in Modern Engineering

**Docker** is an open-source containerization platform that packages applications and all their dependencies into lightweight, portable, self-contained units called **Containers**.

---

#### 🔑 Key Concepts:
- **Dockerfile:** A text blueprint containing sequential instructions to assemble a Docker image.
- **Docker Image:** An immutable, read-only template used to instantiate runtime containers.
- **Docker Container:** A running, isolated instance of an image executing in user-space.
- **Docker Compose:** A tool for defining and running multi-container applications with shared networking and volumes.

---

#### 💡 Portfolio Action Item:
Containerize your existing projects using a multi-stage `Dockerfile` and `docker-compose.yml` to prove production readiness.
"""

    response = f"""### 🎯 Personalized Career Growth Roadmap: **{target_career}**

---

#### 🌟 1. Verified Profile Strengths
- **Matched Skills:** {', '.join(matched) if matched else 'None directly detected in current profile'}
- **Existing Projects:** {', '.join(projects) if projects else 'No portfolio projects registered yet'}

---

#### 🔍 2. High-Priority Skill Gap Analysis
The following critical competencies are required to reach full competitiveness in the **{target_career}** track:
{chr(10).join([f"- **{s}**: High-demand industry standard requirement." for s in missing[:5]])}

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

RETRIEVED EXPERT RAG KNOWLEDGE BASE CHUNKS:
{rag_context}
"""
    
    full_messages = [
        {"role": "system", "content": f"{sys_prompt}\n\n{context_str}"}
    ]
    
    for m in messages[-8:]:
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
                    "temperature": 0.35,
                    "max_tokens": 1800
                },
                timeout=18
            )
            if res.status_code == 200:
                data = res.json()
                content = data["choices"][0]["message"]["content"]
                if content and len(content.strip()) > 10:
                    # Strip any internal think tags cleanly
                    clean_content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
                    if '<think>' in clean_content:
                        clean_content = re.sub(r'<think>.*', '', clean_content, flags=re.DOTALL).strip()
                    if not clean_content and '</think>' in content:
                        clean_content = content.split('</think>')[-1].strip()
                    return clean_content if clean_content else content.strip()
        except Exception as e:
            print(f"Chatbot model {model_name} error: {e}")
            continue
            
    return generate_deterministic_advice(last_user_message, candidate_profile, target_career)
