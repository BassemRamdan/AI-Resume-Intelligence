"""
CareerLens AI - FastAPI Backend Service.
Provides persistent, cached model inference for resume extraction and deterministic career fit mapping.
"""

import os
import shutil
import tempfile
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from lib.resume import extract_resume, get_gliner_model
from lib.models import get_classifier_model, get_embedder_model, get_embedding_resources, classify_text
from lib.career import calculate_career_fit

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
