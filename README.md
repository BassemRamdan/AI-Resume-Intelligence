# CareerLens AI — AI-Driven Resume Intelligence & Career Recommendation System

CareerLens AI is an academic and production-ready AI pipeline for resume parsing, career domain sequence classification, and deterministic multi-signal career recommendation with zero hallucination.

> [!NOTE]
> CareerLens AI is an **Intelligence & Career Recommendation Engine**, not a job-search or vacancy-matching board.

---

## 🏛️ Pipeline Architecture

```
Resume PDF
  → PyMuPDF Computer Vision Layout Parsing & Text Extraction
  → Heuristic Section Segmentation
  → Zero-Shot Entity Extraction (GLiNER: urchade/gliner_multi-v2.1)
  → Skill Ontology Normalization
  → Structured Candidate Profile (Preserving ALL Projects)
  → Sequence Classification (24-Category Transformer, Test Accuracy: 83.83%, Macro F1: 76.41%)
  → Dense Semantic Encoding (sentence-transformers/all-MiniLM-L6-v2, 384-d)
  → KNN Similar Candidate Benchmarking (data/embeddings.npy: 2,466 x 384)
  → Grounded Career Knowledge Base Taxonomy
  → Multi-Signal Deterministic Career Fit Engine + Relevance Gate
  → Evidence-Backed Groq Natural Language Explanations
```

---

## 🎯 Deterministic Career Fit Formula

Career recommendation is calculated mathematically using verified evidence:

$$\text{Career Fit} = 0.35 \times \text{Skill Match} + 0.20 \times \text{Project Match} + 0.20 \times \text{Semantic Match} + 0.10 \times \text{Education Match} + 0.10 \times \text{Experience Match} + 0.05 \times \text{Classification Signal}$$

### Anti-Hallucination Relevance Gate
If a candidate has 0% direct skill match and 0% project match in a target domain, the semantic score is heavily penalized to prevent unrelated career recommendations.

---

## 📚 5 Canonical Research Notebooks

| Notebook | Purpose | Verified Metrics & Assets |
| :--- | :--- | :--- |
| **`notebooks/01_EDA.ipynb`** | Dataset Audit & Exploratory Data Analysis | 2,484 resumes across 24 categories from `BassemRamdan/data` |
| **`notebooks/02_Preprocessing_and_NLP.ipynb`** | PDF Extraction, Segmentation & Zero-Shot NER | Generates `data/processed_resumes.csv` (2,466 records) |
| **`notebooks/03_Classification.ipynb`** | Baselines vs Transformer Fine-Tuning | Test Acc: **83.83%**, Macro F1: **76.41%** (N=371 test split) |
| **`notebooks/04_Embeddings_and_Similarity.ipynb`** | Dense Semantic Encoding & Prototypes | `data/embeddings.npy` (2,466 x 384) & 24 prototypes |
| **`notebooks/05_Career_Knowledge_Base_and_Fit.ipynb`** | Knowledge Base & Deterministic Fit Engine | 6-Signal formula, Relevance Gate & Case Studies |

---

## 📂 Repository Structure

```
CareerLens-AI/
├── app/                           # Next.js 16 App Router (/upload, /profile, /careers)
├── components/                    # React UI Components (ProfileCard, CareerResults, ResumeUpload)
├── data/
│   ├── metadata.csv               # 2,484 stratified split metadata
│   ├── processed_resumes.csv      # 2,466 processed resumes dataset
│   ├── embeddings.npy             # (2466, 384) dense semantic vectors
│   ├── prototypes.json            # 24 category prototype centroid vectors
│   └── cv_metadata.json           # 2,466 indexed resume summaries
├── lib/
│   ├── resume/                    # Layout extraction, segmentation, GLiNER, ontology
│   ├── models/                    # Cached Sequence Classifier & SentenceTransformer
│   ├── career/                    # Career taxonomy & deterministic fit engine
│   └── llm/                       # Grounded Groq explanation generator & fallback
├── models/
│   └── distilbert-resume-classifier/ # Fine-tuned 24-category sequence classifier
├── notebooks/                     # The 5 canonical academic notebooks
├── prompts/                       # Dedicated anti-hallucination prompt templates
├── main.py                        # Persistent FastAPI backend service
├── requirements.txt
└── package.json
```

---

## 🚀 Quick Start

### 1. Backend Setup (FastAPI)
```bash
pip install -r requirements.txt
python main.py
```
FastAPI server will preload models and start on `http://127.0.0.1:8000`.

### 2. Frontend Setup (Next.js)
```bash
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### 3. Environment Variables
Ensure `.env.local` exists in root:
```env
GROQ_API_KEY=your_groq_api_key
AI_SERVICE_URL=http://127.0.0.1:8000
```
