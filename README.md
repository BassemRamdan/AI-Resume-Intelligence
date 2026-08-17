# CareerLens AI - Intelligent Resume Analyzer

CareerLens AI is an advanced, production-ready AI pipeline for resume parsing, career classification, and semantic matching. Built to handle real-world parsing challenges with zero hallucination.

## Core Features

- **Deterministic Entity Extraction**: Uses `PyMuPDF` for structural layout parsing and `GLiNER` (Named Entity Recognition) to explicitly extract skills, projects, and experiences without the hallucination risks of traditional LLMs.
- **Career Classification**: Employs a fine-tuned `DeBERTa`/`DistilBERT` model on thousands of resumes to predict the primary career category with high confidence.
- **Semantic Job Matching**: Leverages `SentenceTransformers` (`all-MiniLM-L6-v2`) to compute cosine similarity between the candidate's skills/projects and 24 distinct career prototypes.
- **Explainable AI (XAI)**: Breaks down the matching score mathematically (Skills 35%, Projects 20%, Semantic 20%, Education 10%, Experience 10%, Class 5%) for complete transparency.
- **Grounded Verification**: Uses `Groq (LLaMA-3.1)` solely as a JSON formatter and evidence validator, strictly preventing data fabrication.

## Architecture & Pipeline

1. **Upload & Parse**: `lib/resume.py` segments the PDF to avoid cross-section entity bleed (e.g., preventing a header name from being classified as a project).
2. **Entity Extraction**: `GLiNER` extracts technical skills and project details deterministically.
3. **Classification**: `lib/classifier.py` runs the extracted text through DistilBERT to get a structural career signal.
4. **Formatting**: `lib/providers/GroqProvider.ts` forces the extracted data into a strictly typed JSON profile, checking against raw text evidence.
5. **Matching**: `lib/similarity.py` calculates the exact fit percentage and generates actionable career roadmaps.

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- Groq API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd AI-Resume-Intelligence
   ```

2. **Backend Setup:**
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

3. **Frontend Setup:**
   ```bash
   npm install
   npm run dev
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

## Repository Structure

- `/app`: Next.js 14 frontend (App Router) with Tailwind CSS.
- `/lib`: Core Python ML pipeline (`resume.py`, `classifier.py`, `similarity.py`).
- `/notebooks`: Research and Development notebooks containing EDA, data preprocessing, and model fine-tuning.

## Design Philosophy

The system was designed with **Anti-Hallucination** as its core principle. By chaining traditional deterministic ML models (GLiNER, DistilBERT) with LLM formatters (Groq), we achieve sub-second latency while guaranteeing 100% evidence-backed data extraction.
