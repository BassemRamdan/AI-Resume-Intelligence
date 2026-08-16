from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import os
import shutil

from lib.resume import extract_resume
from lib.similarity import calculate_similarity

app = FastAPI(title="CareerLens AI Backend")

# Allow CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set this to the Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CareerMapRequest(BaseModel):
    candidateProfile: dict

@app.post("/api/extract")
async def extract_api(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        
    try:
        # Create a temporary file to save the uploaded PDF
        fd, temp_path = tempfile.mkstemp(suffix=".pdf")
        with os.fdopen(fd, "wb") as f:
            shutil.copyfileobj(file.file, f)
            
        # Extract profile using the library function
        profile = extract_resume(temp_path)
        
        if not profile:
            raise HTTPException(status_code=500, detail="Failed to extract profile.")
            
        # Cleanup temp file
        os.remove(temp_path)
        
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/career-map")
async def career_map_api(request: CareerMapRequest):
    try:
        profile_data = request.candidateProfile
        result = calculate_similarity(profile_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # To run locally: python main.py
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
