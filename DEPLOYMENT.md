# Deployment Architecture & Strategy

CareerLens AI utilizes a decoupled architecture for production to ensure Next.js can be deployed on edge networks (like Vercel) while keeping the heavy ML operations on dedicated infrastructure.

## 1. Next.js Frontend Deployment (Vercel)

The frontend is a standard Next.js 14 application. It can be deployed directly to Vercel.

**Steps:**
1. Push your repository to GitHub.
2. Import the project into Vercel.
3. Configure the following Environment Variables in the Vercel Dashboard:
   - `AI_SERVICE_URL`: The fully qualified URL of your hosted Python API (e.g., `https://api.yourdomain.com`).
   - `AI_SERVICE_TOKEN`: A secure token to authenticate requests to your Python API.
4. Deploy! Vercel will automatically use `npm run build` and launch the application.

*Important:* Because the environment variables are configured on the server, they will NOT be exposed to the client-side browser code. The `RemoteResumeProvider` handles the API forwarding securely on the server side.

## 2. Python AI Backend Deployment

Because ML models (`SentenceTransformers`, `FAISS`, and PDF extraction libraries) are memory intensive and require specific system dependencies (like `poppler` or `pymupdf` C-bindings), the Python scripts must be hosted on a dedicated server or containerized service (e.g., Render, Railway, AWS EC2, or Google Cloud Run).

**Steps:**
1. Wrap the existing scripts (`extract_resume.py` and `job_engine.py`) using a lightweight framework like **FastAPI** or **Flask**.
2. Create three endpoints that match the `RemoteResumeProvider` expectations:
   - `POST /api/extract` (Expects a `multipart/form-data` file upload, returns JSON profile)
   - `POST /api/analyze` (Expects JSON with `jobDescription` and `candidateProfile`, returns match JSON)
   - `POST /api/find` (Expects JSON with `candidateProfile`, returns array of jobs JSON)
3. Ensure the API validates the `Authorization: Bearer <TOKEN>` header against your `AI_SERVICE_TOKEN`.
4. Create a `Dockerfile` for the Python service:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY lib/ai ./lib/ai
   # Add your FastAPI server file here
   CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
   ```
5. Deploy the Docker container to your preferred hosting provider and set its public URL as the `AI_SERVICE_URL` in Vercel.

## 3. Local Development

For local development, simply leave `AI_SERVICE_URL` empty in your `.env` file. 

The `ResumeAnalysisProvider` factory will automatically fallback to the `LocalResumeProvider`, which uses `child_process.spawn()` to execute the Python scripts directly from your local virtual environment without needing a separate API server.
