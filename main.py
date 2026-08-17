"""
CareerLens AI - FastAPI Backend Service.
Provides persistent, cached model inference for resume extraction,
deterministic career fit mapping, and interactive AI Career Advisor chatbot.
"""

import os
import shutil
import tempfile
try:
    from dotenv import load_dotenv
    load_dotenv(".env.local")
    load_dotenv(".env")
except ImportError:
    pass
from contextlib import asynccontextmanager
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from lib.resume import extract_resume, get_gliner_model
from lib.models import get_classifier_model, get_embedder_model, get_embedding_resources, classify_text
from lib.career import calculate_career_fit
from lib.career.taxonomy import CATEGORY_METADATA, CAREER_TAXONOMY, get_career_roadmap, get_all_categories
from lib.llm import chat_career_advisor

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Preload and cache all models and embeddings in memory on startup
    print("Pre-loading and warming up models in memory...")
    try:
        get_gliner_model("cpu")
        get_classifier_model("cpu")
        get_embedder_model("cpu")
        get_embedding_resources()
        print("All ML models, embeddings, and prototypes successfully loaded and cached.")
    except Exception as e:
        print(f"Warning during model warmup: {e}")
    yield

app = FastAPI(title="CareerLens AI Backend", lifespan=lifespan)

# Allow CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CareerMapRequest(BaseModel):
    candidateProfile: dict

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    candidateProfile: Optional[dict] = None
    targetCareer: Optional[str] = None

@app.post("/api/extract")
async def extract_api(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        fd, temp_path = tempfile.mkstemp(suffix=".pdf")
        with os.fdopen(fd, "wb") as f:
            shutil.copyfileobj(file.file, f)
            
        # Extract profile with deterministic classification signal
        profile = extract_resume(temp_path, classifier_fn=classify_text)
        
        if not profile:
            raise HTTPException(status_code=500, detail="Failed to extract profile.")
            
        try:
            os.remove(temp_path)
        except Exception:
            pass
            
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/career-map")
async def career_map_api(request: CareerMapRequest):
    try:
        profile_data = request.candidateProfile
        result = calculate_career_fit(profile_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_api(request: ChatRequest):
    try:
        messages_dict = [{"role": m.role, "content": m.content} for m in request.messages]
        reply = chat_career_advisor(
            messages=messages_dict,
            candidate_profile=request.candidateProfile,
            target_career=request.targetCareer
        )
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/categories")
async def get_categories_api():
    """Returns metadata for all 24 dataset categories and career roles."""
    return {
        "total_categories": len(CATEGORY_METADATA),
        "categories": CATEGORY_METADATA,
        "careers": CAREER_TAXONOMY
    }

@app.get("/api/roadmap/{career_name}")
async def get_roadmap_api(career_name: str):
    """Returns the structured 3-phase roadmap for a specific career."""
    roadmap = get_career_roadmap(career_name)
    return {"career": career_name, "roadmap": roadmap}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
