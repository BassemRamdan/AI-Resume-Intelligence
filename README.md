# CareerLens AI

CareerLens AI is a Resume Intelligence platform that utilizes Machine Learning, NLP, and Semantic Similarity to deterministically map candidate resumes to the most suitable career pathways based on a robust dataset of over 2,400 resumes.

## Problem
Traditional resume parsers often rely on simple keyword matching or hallucination-prone LLMs. CareerLens AI solves this by deploying a strict deterministic pipeline. It extracts facts (Skills, Projects, Education) and maps them against canonical career centroids to provide mathematically grounded career intelligence.

## Datasets
This project was trained and built on a robust 3-Dataset architecture:
1. **[Raw Resumes Dataset](https://huggingface.co/datasets/BassemRamdan/data)**: 2,484+ raw PDFs distributed across 24 distinct career categories.
2. **[Cleaned Resume Entities Dataset](https://huggingface.co/datasets/Youssef-mohamed123/resume_entities)**: The NLP-extracted structured entities (Skills, Projects, Education, Experience).
3. **Career Classification & Taxonomy**: The fine-tuned data enabling the similarity engine to map canonical career centroids and validate skill ontologies.

## Architecture

Our application is designed around a multi-stage AI pipeline:

### 1. NLP Pipeline
When a user uploads a PDF resume:
- `PyMuPDF (fitz)` extracts the raw text and Computer Vision layout hierarchies.
- `GLiNER` (a generalized NER model) extracts specific entities like Skills, Experience, Education, and Projects.
- Regular expressions cross-reference an internal Skill Ontology to prevent hallucinated technologies.

### 2. Classification
A fine-tuned DeBERTa model processes the resume to assign a primary career classification from the 24 available categories in the training set.

### 3. Similarity Engine
- The entire dataset of 2,400 resumes was embedded into vectors using `sentence-transformers/all-MiniLM-L6-v2`.
- Canonical category "prototypes" (centroids) were generated.
- When a new resume is processed, it is mapped against the entire dataset space using K-Nearest Neighbors (KNN).
- The engine calculates Cosine Similarity to find both the most aligned Career Categories and specific Peer Candidate Resumes.

### 4. RAG / Groq Explainability
Once the Python ML backend deterministically calculates the classification and similarity scores, the data is sent to Groq (`llama-3.1-8b-instant`). The LLM acts solely as a RAG (Retrieval-Augmented Generation) Explainer—synthesizing a natural language explanation of *why* the candidate matched, based strictly on the extracted evidence.

---

## Installation & Running

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- `npm` or `pnpm`

### Setup Environment
1. Clone the repository.
2. Install the Node dependencies:
   ```bash
   npm install
   ```
3. Create a Python Virtual Environment and install dependencies:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   pip install pypdf PyMuPDF torch gliner transformers sentence-transformers datasets numpy pandas
   ```
4. Configure `.env.local` (copy from `.env.example`) and add your Groq API key:
   ```env
   GROQ_API_KEY=your_key_here
   ```

### Running the Application
1. (Optional) Run the prototype generator to rebuild dataset embeddings:
   ```bash
   python build_prototypes.py
   ```
2. Start the Next.js development server:
   ```bash
   npm run dev
   ```
3. Navigate to `http://localhost:3000` to upload a test resume.

---

## Notebooks
The ML research for this project is systematically structured in the `notebooks/` directory for reproducibility:
- `01_EDA.ipynb`: Data exploration and distribution analysis.
- `02_Preprocessing.ipynb`: Text cleaning and train/test splitting.
- `03_NLP_Extraction.ipynb`: Entity Extraction via GLiNER.
- `04_Baseline.ipynb`: Classical TF-IDF + Logistic Regression baseline.
- `05_FineTuning.ipynb`: Transformer fine-tuning against the baseline.
- `06_Career_Similarity.ipynb`: Embedding generation and prototype cosine similarity logic.

## Future Work
- Expanding the Skill Ontology.
- Enhancing the LayoutLM multimodal component for parsing non-standard resume formats.
