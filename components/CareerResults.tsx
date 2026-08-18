"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { 
  Sparkles, 
  Navigation, 
  CheckCircle2, 
  ChevronRight, 
  Activity, 
  Users, 
  AlertCircle, 
  Compass, 
  ShieldCheck, 
  Zap, 
  ArrowRight,
  HelpCircle,
  FileCheck,
  AlertTriangle,
  Layers,
  Cpu,
  Fingerprint,
  Info
} from "lucide-react";
import { motion } from "framer-motion";
import { useCandidate } from "@/lib/store/CandidateStore";
import CareerChatbot from "@/components/CareerChatbot";

export default function CareerResults() {
  const { profile, isHydrated } = useCandidate();
  const [careerData, setCareerData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (isHydrated && profile && !careerData && !loading) {
      setLoading(true);
      fetchCareerMap(profile);
    } else if (isHydrated && !profile) {
      setError("No profile data found. Please upload a resume PDF first.");
    }
  }, [isHydrated, profile, careerData, loading]);

  const fetchCareerMap = async (candidateProfile: any) => {
    try {
      const response = await fetch("/api/careers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ candidateProfile }),
      });

      if (!response.ok) {
        let errorMsg = "Failed to fetch career analysis.";
        try {
          const errorData = await response.json();
          if (errorData.error) errorMsg = errorData.error;
        } catch (e) {}
        throw new Error(errorMsg);
      }

      const data = await response.json();
      setCareerData(data);
    } catch (err: any) {
      setError(err.message || "An error occurred while communicating with the career engine.");
    } finally {
      setLoading(false);
    }
  };

  if (error) {
    return (
      <div className="container mx-auto px-4 py-24 text-center max-w-lg">
        <div className="w-16 h-16 bg-rose-950/60 text-rose-400 border border-rose-800 rounded-3xl flex items-center justify-center mx-auto mb-6">
          <AlertTriangle className="w-8 h-8" />
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-white mb-2">Analysis Unavailable</h2>
        <p className="text-slate-400 mb-8 text-sm">{error}</p>
        <Link 
          href="/upload" 
          className="inline-flex items-center gap-2 px-8 py-3.5 bg-gradient-to-r from-indigo-600 to-violet-600 text-white rounded-2xl font-bold hover:shadow-lg transition-all"
        >
          <span>Upload Resume</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[65vh] px-4">
        <div className="relative mb-6">
          <div className="w-20 h-20 rounded-3xl bg-slate-900 border border-slate-700 flex items-center justify-center text-cyan-400 shadow-xl">
            <Activity className="w-10 h-10 animate-pulse" />
          </div>
          <motion.div 
            className="absolute -inset-2 border-2 border-cyan-400/60 rounded-3xl"
            animate={{ scale: [1, 1.15, 1], opacity: [1, 0, 1] }}
            transition={{ repeat: Infinity, duration: 2 }}
          />
        </div>
        <h2 className="text-2xl font-black text-white mb-2">Computing Deterministic Career Fit</h2>
        <p className="text-slate-400 text-sm max-w-md text-center leading-relaxed">
          Evaluating 6 independent signals across 28 specialized career tracks & querying Groq 120B for grounded explanations...
        </p>
      </div>
    );
  }

  if (!careerData || !careerData.similarity_engine || !careerData.analysis) {
    return null;
  }

  const engine = careerData.similarity_engine;
  const analysis = careerData.analysis;

  return (
    <div className="container mx-auto px-4 py-10 max-w-6xl">
      {/* Header Banner */}
      <div className="text-center mb-12 space-y-3">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-cyan-400 text-xs font-bold uppercase tracking-wider shadow-sm">
          <Sparkles className="w-3.5 h-3.5" /> 6-Signal Deterministic Career Intelligence
        </div>
        <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-white">
          Career Fit & Recommendation Map
        </h1>
        <p className="text-slate-300 max-w-2xl mx-auto text-sm sm:text-base">
          Primary career recommendations computed using verified evidence: <strong>35% Skills + 20% Projects + 20% Semantic Prototype + 10% Edu + 10% Exp + 5% Classifier</strong>.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
        
        {/* Left Column: Supporting AI Signals (Clearly Framed) */}
        <div className="lg:col-span-1 flex flex-col gap-6">
          
          {/* Domain Classification Signal Card (Clearly Labeled as 5% Signal) */}
          <div className="glass-cyber-card rounded-3xl p-6 md:p-7 text-white relative overflow-hidden border border-slate-800 shadow-xl space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-indigo-400" />
                AI Domain Signal
              </span>
              <span className="text-[10px] font-bold uppercase px-2 py-0.5 rounded-md bg-indigo-950 text-indigo-300 border border-indigo-800/80">
                5% Fit Weight
              </span>
            </div>

            <div>
              <p className="text-[11px] text-slate-400 uppercase tracking-wide">Macro Dataset Category</p>
              <h3 className="text-2xl font-black text-white mt-0.5">
                {engine.classification?.category || "General"}
              </h3>
            </div>

            <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-xl bg-slate-900/90 text-indigo-300 text-xs font-semibold border border-slate-800">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
              <span>
                {engine.classification?.confidence 
                  ? `${(engine.classification.confidence * 100).toFixed(1)}% Classifier Signal` 
                  : "DeBERTa 24-Class Model"}
              </span>
            </div>

            <p className="text-xs text-slate-300 leading-relaxed border-t border-slate-800/80 pt-3">
              {analysis.classification_analysis || "The macro domain classifier provides a supporting 5% baseline signal. Full candidate compatibility is computed across the 28 specialized tracks on the right."}
            </p>
          </div>
          
          {/* KNN Peer Resumes Card (Clearly Labeled as Vector Proximity) */}
          {engine.similar_cvs && engine.similar_cvs.length > 0 && (
            <div className="glass-cyber-card rounded-3xl p-6 md:p-7 border border-slate-800 shadow-sm space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 bg-slate-900 border border-slate-700 rounded-xl flex items-center justify-center text-cyan-400 shadow-sm">
                    <Users className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">KNN Vector Peer Group</h3>
                    <p className="text-[11px] text-slate-400">384-dim Embedding Proximity</p>
                  </div>
                </div>
                <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/80 px-2 py-0.5 rounded-md border border-cyan-800/60">
                  Top 3
                </span>
              </div>

              <div className="p-2.5 rounded-xl bg-slate-900/80 border border-slate-800 text-[11px] text-slate-300 flex items-start gap-2">
                <Info className="w-3.5 h-3.5 text-cyan-400 flex-shrink-0 mt-0.5" />
                <p>Benchmark resumes in the 2,466 dataset with closest document embeddings. Demonstrates semantic cluster density.</p>
              </div>

              <div className="space-y-2.5 pt-1">
                {engine.similar_cvs.map((cv: any, idx: number) => (
                  <div key={idx} className="p-3 rounded-2xl border border-slate-800/80 bg-slate-900/50 hover:bg-slate-900/90 transition-colors space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-bold text-white">{cv.category}</span>
                      <span className="text-[11px] font-black text-cyan-400 bg-slate-950 px-2 py-0.5 rounded-md border border-slate-800">
                        {cv.score}% Cosine
                      </span>
                    </div>
                    {cv.skills && (
                      <p className="text-[10px] text-slate-400 truncate">
                        Keywords: {cv.skills}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Right Column: TOP CAREER RECOMMENDATIONS (The Main Showcase) */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <div className="space-y-0.5">
              <h2 className="text-xl sm:text-2xl font-black text-white flex items-center gap-2">
                <ShieldCheck className="w-6 h-6 text-cyan-400" />
                <span>Top Career Recommendations</span>
              </h2>
              <p className="text-xs text-slate-400">Ranked by 6-Signal Deterministic Formula & Anti-Hallucination Gate</p>
            </div>
            <span className="text-xs font-bold text-cyan-300 bg-cyan-950/80 border border-cyan-800/80 px-3 py-1 rounded-full">
              Top 3 Matches
            </span>
          </div>
          
          <div className="space-y-6">
            {(engine.career_fit || []).slice(0, 3).map((engineData: any, idx: number) => {
              const aiExplanation = analysis.top_careers?.find((c: any) => c.career === engineData.career) || {
                career: engineData.career,
                why: `Evaluated with ${engineData.total_fit}% compatibility based on verified skills, experience, and prototype similarity.`,
                missing_evidence: engineData.evidence?.missing_skills?.length > 0 
                  ? `Recommended growth in: ${engineData.evidence.missing_skills.slice(0, 3).join(', ')}.`
                  : "Strong alignment with core criteria."
              };
              
              const numericScore = engineData.total_fit || 0;
              const careerName = engineData.career;
              
              const rankLabels = ["#1 Primary Recommended Track", "#2 Alternative Career Path", "#3 Adjacent Specialization"];
              
              return (
                <motion.div 
                  key={idx}
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: idx * 0.1 }}
                  className={`glass-cyber-card rounded-3xl p-6 md:p-8 border shadow-xl space-y-5 ${
                    idx === 0 
                      ? "border-indigo-500/50 bg-slate-900/90 shadow-indigo-500/10" 
                      : "border-slate-800 shadow-black/40"
                  }`}
                >
                  <div className="flex flex-wrap sm:flex-nowrap justify-between items-start gap-4">
                    <div className="space-y-1">
                      <span className={`text-[11px] font-extrabold uppercase px-2.5 py-0.5 rounded-md border ${
                        idx === 0 
                          ? "bg-emerald-950 text-emerald-300 border-emerald-700/80" 
                          : "bg-slate-900 text-slate-400 border-slate-700"
                      }`}>
                        {rankLabels[idx]}
                      </span>
                      <h3 className="text-2xl sm:text-3xl font-black text-white mt-1">{careerName}</h3>
                    </div>
                    <div className="flex flex-col items-end">
                      <span className="text-3xl sm:text-4xl font-black text-cyan-400 tracking-tight">
                        {numericScore.toFixed(1)}%
                      </span>
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Computed Fit</span>
                    </div>
                  </div>
                  
                  {/* Progress Bar with 3-Color Gradients */}
                  <div className="w-full h-2.5 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                    <motion.div 
                      initial={{ width: 0 }}
                      animate={{ width: `${Math.min(100, numericScore)}%` }}
                      transition={{ duration: 1.2, delay: idx * 0.15 }}
                      className={`h-full rounded-full ${
                        numericScore >= 70 
                          ? "bg-gradient-to-r from-emerald-400 via-cyan-400 to-indigo-500" 
                          : numericScore >= 45 
                            ? "bg-gradient-to-r from-indigo-500 via-violet-500 to-cyan-400" 
                            : "bg-gradient-to-r from-amber-400 to-indigo-500"
                      }`}
                    />
                  </div>

                  {/* 6-Signal Mathematical Gauge Grid */}
                  <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 p-3.5 bg-slate-950/80 rounded-2xl border border-slate-800/90 text-xs">
                    <div className="p-2.5 bg-slate-900/90 rounded-xl border border-slate-800 shadow-xs">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Skills (35%)</span>
                      <p className="text-sm font-black text-indigo-300 mt-0.5">{engineData.breakdown?.skill_match}%</p>
                    </div>
                    <div className="p-2.5 bg-slate-900/90 rounded-xl border border-slate-800 shadow-xs">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Projects (20%)</span>
                      <p className="text-sm font-black text-violet-300 mt-0.5">{engineData.breakdown?.project_match}%</p>
                    </div>
                    <div className="p-2.5 bg-slate-900/90 rounded-xl border border-slate-800 shadow-xs">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Prototype (20%)</span>
                      <p className="text-sm font-black text-cyan-300 mt-0.5">{engineData.breakdown?.semantic_match}%</p>
                    </div>
                    <div className="p-2.5 bg-slate-900/90 rounded-xl border border-slate-800 shadow-xs">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Education (10%)</span>
                      <p className="text-sm font-black text-emerald-300 mt-0.5">{engineData.breakdown?.education_match}%</p>
                    </div>
                    <div className="p-2.5 bg-slate-900/90 rounded-xl border border-slate-800 shadow-xs">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Experience (10%)</span>
                      <p className="text-sm font-black text-amber-300 mt-0.5">{engineData.breakdown?.experience_match}%</p>
                    </div>
                    <div className="p-2.5 bg-slate-900/90 rounded-xl border border-slate-800 shadow-xs">
                      <span className="text-[10px] text-slate-400 font-bold uppercase">Classifier (5%)</span>
                      <p className="text-sm font-black text-rose-300 mt-0.5">{engineData.breakdown?.classification_signal}%</p>
                    </div>
                  </div>

                  {/* AI Grounded Justification */}
                  <p className="text-slate-300 text-xs sm:text-sm leading-relaxed font-normal">
                    {aiExplanation.why}
                  </p>
                  
                  {/* Missing Skills Warning Pill */}
                  <div className="text-rose-200 text-xs leading-relaxed bg-rose-950/50 p-3.5 rounded-2xl border border-rose-900/80 space-y-1">
                    <span className="font-bold uppercase tracking-wider text-[10px] text-rose-400 block">Critical Skill Gaps to Close:</span>
                    <p>{aiExplanation.missing_evidence}</p>
                  </div>

                  {/* Matched Evidence Chips */}
                  <div className="bg-slate-950/80 border border-slate-800/80 rounded-2xl p-4">
                    <h5 className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2.5">Verified Matched Credentials</h5>
                    <div className="flex flex-wrap gap-1.5">
                      {engineData.evidence?.matched_skills?.map((evidence: string, i: number) => (
                        <span key={i} className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-emerald-950/80 text-emerald-300 text-xs border border-emerald-600/40 font-semibold">
                          <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                          <span>{evidence}</span>
                        </span>
                      ))}
                      {engineData.evidence?.matched_projects?.map((evidence: string, i: number) => (
                        <span key={i} className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-indigo-950/80 text-indigo-300 text-xs border border-indigo-600/40 font-semibold">
                          <CheckCircle2 className="w-3 h-3 text-indigo-400" />
                          <span>{evidence}</span>
                        </span>
                      ))}
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
      
      <div className="text-center pb-12 flex flex-col sm:flex-row items-center justify-center gap-4">
        <Link 
          href="/profile" 
          className="inline-flex items-center gap-2 px-6 py-3.5 bg-slate-900 text-white rounded-2xl font-bold border border-slate-700 shadow-md hover:bg-slate-800 transition-all text-sm hover:scale-105"
        >
          <span>Review Extracted Profile</span>
          <ChevronRight className="w-4 h-4" />
        </Link>
        <Link 
          href="/upload" 
          className="inline-flex items-center gap-2 px-6 py-3.5 bg-gradient-to-r from-indigo-600 to-cyan-600 text-white rounded-2xl font-bold hover:shadow-lg transition-all text-sm hover:scale-105"
        >
          <span>Analyze Another Resume</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {/* Floating AI Career Advisor Chatbot */}
      <CareerChatbot 
        candidateProfile={profile} 
        topCareers={engine.career_fit || []} 
      />
    </div>
  );
}
