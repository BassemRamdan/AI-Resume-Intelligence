"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { 
  Upload, 
  FileText, 
  CheckCircle2, 
  Loader2, 
  AlertCircle, 
  Sparkles, 
  Cpu, 
  ShieldCheck, 
  FileCheck,
  Zap,
  ArrowRight,
  Play
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useCandidate } from "@/lib/store/CandidateStore";

export default function ResumeUpload() {
  const { setProfile } = useCandidate();
  const [file, setFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [status, setStatus] = useState<"idle" | "uploading" | "extracting" | "analyzing" | "building" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (selectedFile: File) => {
    setStatus("idle");
    setErrorMessage("");
    if (selectedFile.type !== "application/pdf") {
      setStatus("error");
      setErrorMessage("Only PDF resume files are supported.");
      return;
    }
    if (selectedFile.size > 5 * 1024 * 1024) {
      setStatus("error");
      setErrorMessage("File size exceeds 5MB limit. Please upload a smaller PDF.");
      return;
    }
    setFile(selectedFile);
  };

  const processResume = async (fileToUpload?: File) => {
    const targetFile = fileToUpload || file;
    if (!targetFile) return;

    try {
      setStatus("uploading");
      
      const formData = new FormData();
      formData.append("resume", targetFile);

      setTimeout(() => setStatus("extracting"), 700);
      setTimeout(() => setStatus("analyzing"), 1800);
      setTimeout(() => setStatus("building"), 3000);

      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        let errorMsg = `Server error (${response.status})`;
        try {
          const errorData = await response.json();
          if (errorData.error) errorMsg = errorData.error;
        } catch (e) {}
        throw new Error(errorMsg);
      }

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      setProfile(data);
      setStatus("success");
      
      setTimeout(() => {
        router.push("/profile");
      }, 900);

    } catch (err: any) {
      console.error(err);
      setStatus("error");
      setErrorMessage(err.message || "An unexpected error occurred while processing your resume. Please verify that FastAPI is running on port 8000.");
    }
  };

  const loadSampleResume = () => {
    const sampleProfile = {
      identity: {
        name: "Bassem Ramadan",
        email: "bassem@example.com",
        phone: "+20 100 000 0000",
        location: "Alexandria, Egypt"
      },
      summary: "Aspiring AI & Software Engineer with hands-on experience in full-stack development, machine learning, and database design.",
      skills: [
        { name: "Python", normalized_name: "Python", category: "Technical", evidence: "Python project", confidence: 0.95 },
        { name: "Machine Learning", normalized_name: "Machine Learning", category: "Technical", evidence: "ML algorithms", confidence: 0.95 },
        { name: "Streamlit", normalized_name: "Streamlit", category: "Technical", evidence: "Streamlit UI", confidence: 0.95 },
        { name: "React", normalized_name: "React", category: "Technical", evidence: "React.js frontend", confidence: 0.95 },
        { name: "Node.js", normalized_name: "Node.js", category: "Technical", evidence: "Node.js backend", confidence: 0.95 },
        { name: "Express", normalized_name: "Express", category: "Technical", evidence: "Express APIs", confidence: 0.95 },
        { name: "SQL", normalized_name: "SQL", category: "Technical", evidence: "SQL normalization", confidence: 0.95 },
        { name: "NLP", normalized_name: "NLP", category: "Technical", evidence: "NLP emotion classification", confidence: 0.95 },
        { name: "Data Analysis", normalized_name: "Data Analysis", category: "Technical", evidence: "Data visualization", confidence: 0.95 },
        { name: "RESTful APIs", normalized_name: "RESTful APIs", category: "Technical", evidence: "RESTful endpoints", confidence: 0.95 }
      ],
      soft_skills: [
        "Problem Solving", "Teamwork", "Communication", "Time Management", "Analytical Thinking", "Adaptability", "Fast Learner"
      ],
      education: [
        {
          institution: "Alexandria National University",
          degree: "Bachelor of Computer Science",
          field: "Computer Science / Technical",
          evidence: "Alexandria National University",
          confidence: 0.90
        }
      ],
      experience: [],
      projects: [
        {
          name: "Movie Recommendation System (Python • Machine Learning • Streamlit)",
          description: "Built an interactive Streamlit interface. Implemented content-based recommendation algorithms and integrated movie datasets and similarity models. Improved recommendation accuracy through feature engineering.",
          technologies: ["Python", "Machine Learning", "Streamlit"],
          role: "Lead Developer",
          links: [],
          evidence: "Movie Recommendation System",
          confidence: 0.90
        },
        {
          name: "MindCare AI – Emotion Detection (Python • Machine Learning)",
          description: "Built an emotion classification system using NLP techniques. Trained classification models on large emotion datasets with text preprocessing, feature extraction, and ML evaluation metrics.",
          technologies: ["Python", "NLP", "Machine Learning"],
          role: "Developer",
          links: [],
          evidence: "MindCare AI",
          confidence: 0.90
        },
        {
          name: "Student Study Spaces Analysis (Python • Data Analysis)",
          description: "Conducted data analysis on university study spaces. Generated insights using visualization tools and created reports supporting decision-making.",
          technologies: ["Python", "Data Analysis"],
          role: "Data Analyst",
          links: [],
          evidence: "Student Study Spaces Analysis",
          confidence: 0.90
        },
        {
          name: "Hospital Database Management System (SQL • Database Design)",
          description: "Designed a complete relational database. Created ER diagrams, developed SQL queries and normalization, and implemented entity relationships and constraints.",
          technologies: ["SQL", "Database Design"],
          role: "Database Designer",
          links: [],
          evidence: "Hospital Database Management System",
          confidence: 0.90
        },
        {
          name: "Full Stack Web Applications (React.js • Node.js • Express)",
          description: "Developed responsive web applications. Built RESTful APIs, connected frontend with backend services, and managed authentication and CRUD operations.",
          technologies: ["React", "Node.js", "Express", "RESTful APIs"],
          role: "Full Stack Developer",
          links: [],
          evidence: "Full Stack Web Applications",
          confidence: 0.90
        }
      ],
      certifications: [
        { name: "Full Stack Web Development (React & Node.js)", issuer: "Professional Credential", date: "Verified", evidence: "Full Stack Web Development", confidence: 0.95 },
        { name: "Artificial Intelligence Fundamentals", issuer: "Professional Credential", date: "Verified", evidence: "Artificial Intelligence Fundamentals", confidence: 0.95 },
        { name: "Machine Learning Fundamentals", issuer: "Professional Credential", date: "Verified", evidence: "Machine Learning Fundamentals", confidence: 0.95 },
        { name: "Data Analysis using Python", issuer: "Professional Credential", date: "Verified", evidence: "Data Analysis using Python", confidence: 0.95 }
      ],
      languages: [
        { language: "English", proficiency: "Professional Working Proficiency" },
        { language: "Arabic", proficiency: "Native" }
      ],
      career_signal: {
        dataset_category: "INFORMATION-TECHNOLOGY",
        confidence: 0.85
      },
      filename: "Bassem_Ramadan_Resume.pdf",
      raw_text_snippet: "Bassem Ramadan Alexandria National University Computer Science Python Machine Learning Streamlit React Node.js Express SQL NLP Data Analysis"
    };

    setStatus("extracting");
    setTimeout(() => setStatus("analyzing"), 600);
    setTimeout(() => setStatus("building"), 1200);
    setTimeout(() => {
      setProfile(sampleProfile);
      setStatus("success");
      setTimeout(() => router.push("/profile"), 700);
    }, 1800);
  };

  const steps = [
    { id: "uploading", label: "01 Uploading Document & Layout Parsing (PyMuPDF)" },
    { id: "extracting", label: "02 Zero-Shot Entity Extraction (GLiNER v2.1 & Ontology)" },
    { id: "analyzing", label: "03 Domain Sequence Classification (DeBERTa 24-Class)" },
    { id: "building", label: "04 Dense Vector Embedding (SentenceTransformers 384-dim)" },
  ];

  const currentStepIndex = steps.findIndex(s => s.id === status);

  return (
    <div className="container mx-auto max-w-4xl px-4 py-12 md:py-20">
      <div className="text-center mb-10 space-y-3">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-cyan-400 text-xs font-bold uppercase tracking-wider shadow-sm">
          <Sparkles className="w-3.5 h-3.5" /> Deterministic Extraction Pipeline
        </div>
        <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-white">
          Upload Your Resume PDF
        </h1>
        <p className="text-slate-400 max-w-lg mx-auto text-sm sm:text-base">
          Our multi-model engine will extract your verified skills, classify your domain, and compute deterministic career fit scores.
        </p>
      </div>

      <div className="glass-cyber-card rounded-3xl p-8 md:p-12 border border-slate-800 shadow-2xl space-y-6">
        
        {status === "idle" || status === "error" ? (
          <>
            <div 
              className={`border-2 border-dashed rounded-3xl p-10 md:p-14 text-center transition-all cursor-pointer ${
                dragActive 
                  ? "border-cyan-400 bg-cyan-950/30 scale-[1.01] shadow-lg shadow-cyan-500/20" 
                  : "border-slate-700/80 hover:border-indigo-500 hover:bg-slate-900/60"
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handleChange}
                className="hidden"
              />
              
              <div className="mx-auto w-20 h-20 rounded-3xl bg-slate-900 border border-slate-700 flex items-center justify-center mb-6 text-cyan-400 shadow-inner">
                <Upload className="w-10 h-10 animate-bounce" style={{ animationDuration: '3s' }} />
              </div>
              
              <h3 className="text-xl sm:text-2xl font-bold text-white mb-2">
                {file ? file.name : "Drag & drop your resume PDF here"}
              </h3>
              <p className="text-sm text-slate-400 mb-6 max-w-sm mx-auto">
                {file ? `Selected file (${(file.size / 1024).toFixed(1)} KB) - Ready to analyze` : "Supports text-based PDF format, up to 5MB file size"}
              </p>
              
              <div className="inline-flex items-center gap-2 px-6 py-3 bg-slate-900 border border-slate-700 text-white rounded-2xl font-bold text-sm shadow-md hover:bg-slate-800 transition-colors pointer-events-none">
                <FileCheck className="w-4 h-4 text-cyan-400" />
                <span>{file ? "Change File" : "Browse Computer"}</span>
              </div>
            </div>

            {/* Quick Demo Resume Button */}
            <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
              <span className="text-xs text-slate-500 font-medium">Or test with one click:</span>
              <button
                type="button"
                onClick={loadSampleResume}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-cyan-300 border border-cyan-800/60 text-xs font-bold transition-all shadow-xs hover:scale-105 active:scale-95"
              >
                <Play className="w-3.5 h-3.5 text-cyan-400 fill-cyan-400" />
                <span>Load Sample CS/AI Resume (Instant Demo)</span>
              </button>
            </div>
          </>
        ) : null}

        {status === "error" && (
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-5 rounded-2xl bg-rose-950/60 border border-rose-800/80 flex items-start gap-3.5 text-rose-200"
          >
            <AlertCircle className="w-5 h-5 shrink-0 text-rose-400 mt-0.5" />
            <div>
              <h4 className="font-bold text-sm text-rose-100">Extraction Pipeline Warning</h4>
              <p className="text-xs sm:text-sm mt-1 text-rose-300">{errorMessage}</p>
            </div>
          </motion.div>
        )}

        {file && (status === "idle" || status === "error") && (
          <div className="pt-4 flex justify-center">
            <button 
              onClick={() => processResume()}
              className="w-full sm:w-auto px-10 py-4 bg-gradient-to-r from-indigo-600 via-violet-600 to-cyan-600 text-white rounded-2xl font-black text-base hover:shadow-xl hover:shadow-indigo-500/40 hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-3"
            >
              <Zap className="w-5 h-5 text-amber-300" />
              <span>Launch Multi-Model Analysis</span>
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        )}

        {(status !== "idle" && status !== "error") && (
          <div className="py-8 px-2 md:px-6">
            <div className="flex items-center justify-center mb-10">
              <div className="relative">
                <div className={`w-20 h-20 rounded-3xl flex items-center justify-center shadow-lg transition-colors ${
                  status === "success" 
                    ? "bg-emerald-500 text-white shadow-emerald-500/40" 
                    : "bg-indigo-600 text-white shadow-indigo-500/40"
                }`}>
                  <FileText className="w-10 h-10" />
                </div>
                {status !== "success" && (
                  <motion.div 
                    className="absolute -inset-2 rounded-3xl border-2 border-cyan-400/60"
                    animate={{ scale: [1, 1.15, 1], opacity: [1, 0, 1] }}
                    transition={{ repeat: Infinity, duration: 2.2 }}
                  />
                )}
              </div>
            </div>

            <div className="max-w-xl mx-auto space-y-4">
              {steps.map((step, idx) => {
                const isComplete = status === "success" || currentStepIndex > idx;
                const isActive = currentStepIndex === idx && status !== "success";
                
                return (
                  <div 
                    key={step.id} 
                    className={`flex items-center gap-4 p-4 rounded-2xl border transition-all ${
                      isComplete 
                        ? "bg-emerald-950/50 border-emerald-500/40 text-emerald-200" 
                        : isActive 
                          ? "bg-indigo-950/70 border-indigo-500/60 shadow-lg shadow-indigo-500/20 text-white" 
                          : "bg-slate-900/40 border-slate-800/60 text-slate-500 opacity-60"
                    }`}
                  >
                    <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 font-bold ${
                      isComplete 
                        ? "bg-emerald-500 text-white" 
                        : isActive 
                          ? "bg-indigo-600 text-white" 
                          : "bg-slate-800 text-slate-400"
                    }`}>
                      {isComplete ? (
                        <CheckCircle2 className="w-5 h-5" />
                      ) : isActive ? (
                        <Loader2 className="w-5 h-5 animate-spin text-cyan-300" />
                      ) : (
                        <span className="text-xs">{idx + 1}</span>
                      )}
                    </div>
                    <span className="font-semibold text-xs sm:text-sm">
                      {step.label}
                    </span>
                  </div>
                );
              })}
            </div>
            
            <AnimatePresence>
              {status === "success" && (
                <motion.div 
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-8 text-center text-emerald-400 font-bold text-sm flex items-center justify-center gap-2"
                >
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                  <span>Candidate intelligence constructed successfully! Navigating to profile...</span>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  );
}
