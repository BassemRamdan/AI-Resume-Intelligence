"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Sparkles, Navigation, CheckCircle2, ChevronRight, Activity, Users, AlertCircle } from "lucide-react";
import { motion } from "framer-motion";
import { useCandidate } from "@/lib/store/CandidateStore";

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
      setError("No profile data found. Please upload a resume first.");
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
      setError(err.message || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  if (error) {
    return (
      <div className="container mx-auto px-4 py-24 text-center max-w-lg">
        <h2 className="text-2xl font-bold text-slate-900 mb-4">Cannot Generate Analysis</h2>
        <p className="text-slate-500 mb-8">{error}</p>
        <Link href="/upload" className="px-6 py-3 bg-indigo-600 text-white rounded-full font-medium hover:bg-indigo-700 transition-colors">
          Upload Resume
        </Link>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="relative mb-6">
          <Activity className="w-12 h-12 text-indigo-600" />
          <motion.div 
            className="absolute inset-0 border-2 border-indigo-400 rounded-full"
            animate={{ scale: [1, 1.5, 1], opacity: [1, 0, 1] }}
            transition={{ repeat: Infinity, duration: 2 }}
          />
        </div>
        <h2 className="text-xl font-bold text-slate-900 mb-2">Computing Career Fit</h2>
        <p className="text-slate-500 text-sm max-w-sm text-center">Analyzing skills, projects, and semantic alignment against deterministic career profiles...</p>
      </div>
    );
  }

  if (!careerData || !careerData.similarity_engine || !careerData.analysis) {
    return null;
  }

  const engine = careerData.similarity_engine;
  const analysis = careerData.analysis;

  return (
    <div className="container mx-auto px-4 py-12 max-w-6xl">
      <div className="text-center mb-16">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 text-indigo-600 text-sm font-medium mb-6 border border-indigo-100">
          <Sparkles className="w-4 h-4" /> Deterministic Recommendation Engine
        </div>
        <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 mb-4">
          Career Fit Analysis
        </h1>
        <p className="text-lg text-slate-500 max-w-2xl mx-auto">
          We computed your multi-signal career compatibility based on skills, projects, education, and semantic similarity.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
        <div className="lg:col-span-1 flex flex-col gap-8">
           <div className="bg-slate-900 rounded-3xl p-8 text-white relative overflow-hidden">
             <div className="absolute top-0 right-0 p-6 opacity-10">
                <Navigation className="w-32 h-32" />
             </div>
             <p className="text-slate-400 text-sm uppercase tracking-wider font-bold mb-2">Primary Classification</p>
             <h2 className="text-3xl font-black mb-4 text-white leading-tight">
               {engine.classification?.category || "Unknown"}
             </h2>
             <div className="inline-flex items-center gap-2 px-3 py-1 rounded-lg bg-indigo-500/20 text-indigo-300 font-semibold mb-6">
                {engine.classification?.confidence ? `${(engine.classification.confidence * 100).toFixed(1)}% Confidence` : "Confidence unavailable"}
             </div>
             <p className="text-slate-300 text-sm leading-relaxed relative z-10">
               {analysis.classification_analysis}
             </p>
           </div>
           
           {/* Similar CVs Dataset Cluster */}
           {engine.similar_cvs && engine.similar_cvs.length > 0 && (
             <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 bg-indigo-50 rounded-lg text-indigo-600">
                     <Users className="w-6 h-6" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-900">Similar Resumes</h3>
                </div>
                <div className="mb-4 inline-flex items-center gap-2 px-2 py-1 bg-amber-50 text-amber-700 text-xs font-bold uppercase rounded border border-amber-200">
                  <AlertCircle className="w-3 h-3" /> Semantic Similarity — Not Career Recommendation
                </div>
                <p className="text-sm text-slate-500 mb-6 leading-relaxed">
                  {analysis.similar_profiles_analysis}
                </p>
                <div className="space-y-4">
                  {engine.similar_cvs.map((cv: any, idx: number) => (
                    <div key={idx} className="p-4 rounded-xl border border-slate-100 bg-slate-50 hover:border-indigo-200 transition-colors">
                       <div className="flex justify-between items-start mb-2">
                          <div>
                            <span className="text-xs font-bold text-slate-400 uppercase">Resume #{cv.id}</span>
                            <h4 className="font-bold text-slate-800">{cv.category}</h4>
                          </div>
                          <div className="bg-white px-2 py-1 rounded text-sm font-bold text-indigo-600 shadow-sm border border-slate-100">
                            {cv.score}%
                          </div>
                       </div>
                    </div>
                  ))}
                </div>
             </div>
           )}
        </div>

        <div className="lg:col-span-2 space-y-6">
          <h3 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            Top Career Fit <span className="text-slate-400 font-normal text-sm ml-2">(Deterministic Scoring)</span>
          </h3>
          
          <div className="space-y-6">
            {analysis.top_careers?.map((careerData: any, idx: number) => {
              // Find matching deterministic data from the engine
              const engineData = engine.career_fit?.find((c:any) => c.career === careerData.career) || {
                total_fit: 0,
                breakdown: { skill_match: 0, project_match: 0, semantic_match: 0, education_match: 0, experience_match: 0, classification_signal: 0 },
                evidence: { matched_skills: [], missing_skills: [], matched_projects: [] }
              };
              
              const numericScore = engineData.total_fit;
              
              return (
                <div key={idx} className="bg-white rounded-2xl p-6 border border-slate-100 shadow-sm hover:shadow-md transition-shadow group">
                  <div className="flex flex-wrap md:flex-nowrap justify-between items-start mb-3 gap-4">
                    <div className="flex-1">
                       <h4 className="text-2xl font-bold text-slate-900">{careerData.career}</h4>
                    </div>
                    <div className="flex flex-col items-end">
                       <span className="text-3xl font-black text-indigo-600">{numericScore.toFixed(1)}%</span>
                       <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Career Fit</span>
                    </div>
                  </div>
                  
                  <div className="w-full h-2 bg-slate-100 rounded-full mb-6 overflow-hidden">
                    <motion.div 
                      initial={{ width: 0 }}
                      animate={{ width: numericScore + '%' }}
                      transition={{ duration: 1, delay: idx * 0.1 }}
                      className="h-full bg-gradient-to-r from-indigo-500 to-indigo-600 rounded-full"
                    />
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6 p-4 bg-slate-50 rounded-xl">
                    <div className="flex flex-col">
                      <span className="text-xs text-slate-500 font-medium">Skill Match</span>
                      <span className="text-sm font-bold text-slate-800">{engineData.breakdown.skill_match}%</span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-xs text-slate-500 font-medium">Project Match</span>
                      <span className="text-sm font-bold text-slate-800">{engineData.breakdown.project_match}%</span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-xs text-slate-500 font-medium">Semantic Match</span>
                      <span className="text-sm font-bold text-slate-800">{engineData.breakdown.semantic_match}%</span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-xs text-slate-500 font-medium">Education Match</span>
                      <span className="text-sm font-bold text-slate-800">{engineData.breakdown.education_match}%</span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-xs text-slate-500 font-medium">Experience Match</span>
                      <span className="text-sm font-bold text-slate-800">{engineData.breakdown.experience_match}%</span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-xs text-slate-500 font-medium">Classification Signal</span>
                      <span className="text-sm font-bold text-slate-800">{engineData.breakdown.classification_signal}%</span>
                    </div>
                  </div>

                  <p className="text-slate-600 text-sm mb-4 leading-relaxed font-medium">
                    {careerData.why}
                  </p>
                  
                  <p className="text-rose-600/80 text-sm mb-6 leading-relaxed bg-rose-50 p-3 rounded-lg border border-rose-100">
                    <span className="font-bold">Missing/Weak Evidence:</span> {careerData.missing_evidence}
                  </p>

                  <div className="bg-white border border-slate-100 rounded-xl p-4">
                    <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Matched Evidence</h5>
                    <div className="flex flex-wrap gap-2">
                      {engineData.evidence?.matched_skills?.map((evidence: string, i: number) => (
                        <span key={i} className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-emerald-50 text-emerald-700 text-sm border border-emerald-200 shadow-sm font-medium">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          {evidence}
                        </span>
                      ))}
                      {engineData.evidence?.matched_projects?.map((evidence: string, i: number) => (
                        <span key={i} className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-blue-50 text-blue-700 text-sm border border-blue-200 shadow-sm font-medium">
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          {evidence}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
      
      <div className="text-center pb-12">
        <Link href="/profile" className="inline-flex items-center gap-2 px-6 py-3 bg-white text-slate-900 rounded-full font-bold border border-slate-200 shadow-sm hover:shadow hover:bg-slate-50 transition-all">
          View Extracted Profile <ChevronRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
}
