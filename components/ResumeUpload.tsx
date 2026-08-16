"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { Upload, FileText, CheckCircle2, Loader2, AlertCircle } from "lucide-react";
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
      setErrorMessage("Please upload a PDF file.");
      return;
    }
    if (selectedFile.size > 5 * 1024 * 1024) {
      setStatus("error");
      setErrorMessage("File size must be less than 5MB.");
      return;
    }
    setFile(selectedFile);
  };

  const processResume = async () => {
    if (!file) return;

    try {
      setStatus("uploading");
      
      const formData = new FormData();
      formData.append("resume", file);

      // Simulate quick extraction phase for UX
      setTimeout(() => setStatus("extracting"), 800);
      setTimeout(() => setStatus("analyzing"), 2000);
      setTimeout(() => setStatus("building"), 3500);

      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.error) {
        throw new Error(data.error);
      }

      // Use the context store instead of raw localStorage
      setProfile(data);
      
      setStatus("success");
      setTimeout(() => {
        router.push("/profile");
      }, 1000);

    } catch (err: any) {
      console.error(err);
      setStatus("error");
      setErrorMessage(err.message || "An unexpected error occurred while processing your resume.");
    }
  };

  const steps = [
    { id: "uploading", label: "01 Uploading Resume" },
    { id: "extracting", label: "02 Extracting Information" },
    { id: "analyzing", label: "03 Analyzing Career Profile" },
    { id: "building", label: "04 Building Career Intelligence" },
  ];

  const currentStepIndex = steps.findIndex(s => s.id === status);

  return (
    <div className="container mx-auto max-w-3xl px-4 py-12 md:py-24">
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900 mb-4">Analyze Your Resume</h1>
        <p className="text-slate-500">Upload your PDF resume to generate your evidence-based candidate profile.</p>
      </div>

      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden p-8">
        
        {status === "idle" || status === "error" ? (
          <div 
            className={`border-2 border-dashed rounded-2xl p-12 text-center transition-colors cursor-pointer ${dragActive ? "border-indigo-500 bg-indigo-50/50" : "border-slate-300 hover:border-slate-400 hover:bg-slate-50"}`}
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
            
            <div className="mx-auto w-16 h-16 rounded-full bg-slate-100 flex items-center justify-center mb-6">
              <Upload className="w-8 h-8 text-slate-500" />
            </div>
            
            <h3 className="text-xl font-semibold text-slate-900 mb-2">
              {file ? file.name : "Click or drag to upload"}
            </h3>
            <p className="text-sm text-slate-500 mb-6">
              {file ? "Ready to analyze" : "PDF format only, maximum 5MB"}
            </p>
            
            <button 
              className="px-6 py-3 bg-slate-900 text-white rounded-full font-medium hover:bg-slate-800 transition-colors pointer-events-none"
            >
              Select File
            </button>
          </div>
        ) : null}

        {status === "error" && (
          <div className="mt-6 p-4 rounded-xl bg-red-50 border border-red-100 flex items-start gap-3 text-red-800">
            <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold">Processing Failed</h4>
              <p className="text-sm mt-1">{errorMessage}</p>
            </div>
          </div>
        )}

        {file && (status === "idle" || status === "error") && (
          <div className="mt-8 flex justify-center">
             <button 
              onClick={processResume}
              className="w-full md:w-auto px-10 py-4 bg-indigo-600 text-white rounded-full font-semibold hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-600/20"
            >
              Analyze Resume Intelligence
            </button>
          </div>
        )}

        {(status !== "idle" && status !== "error") && (
          <div className="py-8 px-4">
            <div className="flex items-center justify-center mb-12">
              <div className="relative">
                <FileText className={`w-16 h-16 ${status === "success" ? "text-emerald-500" : "text-indigo-600"}`} />
                {status !== "success" && (
                  <motion.div 
                    className="absolute inset-0 rounded border-2 border-indigo-400"
                    animate={{ scale: [1, 1.2, 1], opacity: [1, 0, 1] }}
                    transition={{ repeat: Infinity, duration: 2 }}
                  />
                )}
              </div>
            </div>

            <div className="max-w-md mx-auto space-y-6">
              {steps.map((step, idx) => {
                const isComplete = status === "success" || currentStepIndex > idx;
                const isActive = currentStepIndex === idx && status !== "success";
                
                return (
                  <div key={step.id} className="flex items-center gap-4">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${isComplete ? "bg-emerald-100 text-emerald-600" : isActive ? "bg-indigo-100 text-indigo-600" : "bg-slate-100 text-slate-400"}`}>
                      {isComplete ? <CheckCircle2 className="w-5 h-5" /> : isActive ? <Loader2 className="w-5 h-5 animate-spin" /> : <div className="w-2.5 h-2.5 rounded-full bg-slate-300" />}
                    </div>
                    <span className={`font-medium ${isComplete ? "text-slate-900" : isActive ? "text-indigo-600" : "text-slate-400"}`}>
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
                    className="mt-12 text-center text-emerald-600 font-medium"
                 >
                   Profile built successfully! Redirecting...
                 </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  );
}
