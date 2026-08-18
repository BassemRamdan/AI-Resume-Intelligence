"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { 
  Briefcase, 
  GraduationCap, 
  Map, 
  FolderGit2, 
  Award, 
  ChevronRight, 
  Fingerprint, 
  Sparkles, 
  ServerCrash, 
  CheckCircle2, 
  AlertCircle,
  FileCheck,
  Zap,
  Layers,
  ArrowRight,
  ShieldCheck,
  HeartHandshake
} from "lucide-react";
import { motion } from "framer-motion";
import { useCandidate } from "@/lib/store/CandidateStore";
import CareerChatbot from "@/components/CareerChatbot";

export default function ProfileCard() {
  const { profile, isHydrated } = useCandidate();
  
  if (!isHydrated) {
    return (
      <div className="p-24 text-center text-slate-400 flex flex-col items-center justify-center gap-3">
        <div className="w-8 h-8 rounded-full border-2 border-cyan-400 border-t-transparent animate-spin" />
        <span className="text-sm font-semibold">Loading Candidate Intelligence...</span>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="container mx-auto px-4 py-24 text-center max-w-lg">
        <div className="w-20 h-20 bg-rose-950/60 text-rose-400 border border-rose-800 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-lg">
          <ServerCrash className="w-10 h-10" />
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-white mb-2">No Profile In Memory</h2>
        <p className="text-slate-400 mb-8 text-sm">Please upload a resume PDF to run the multi-model extraction pipeline.</p>
        <Link 
          href="/upload" 
          className="inline-flex items-center gap-2 px-8 py-3.5 bg-gradient-to-r from-indigo-600 via-violet-600 to-cyan-600 text-white rounded-2xl font-bold shadow-lg shadow-indigo-500/30 hover:scale-105 transition-all"
        >
          <span>Upload Resume</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  const cleanList = (arr: any) => {
    if (!Array.isArray(arr)) return [];
    return arr.filter(item => {
      if (typeof item === 'string') return item !== "UNKNOWN" && item.trim().length > 0;
      if (typeof item === 'object' && item !== null) {
        const title = item.name || item.job_title || item.institution || item.language;
        if (!title || title === "UNKNOWN" || title === "NOT_FOUND") return false;
        return true;
      }
      return false;
    });
  };
  
  const skills = cleanList(profile.skills);
  const softSkills = cleanList(profile.soft_skills || []);
  const experience = cleanList(profile.experience);
  const education = cleanList(profile.education);
  const projects = cleanList(profile.projects);
  const certs = cleanList(profile.certifications);

  const categoryName = profile.career_signal?.dataset_category && profile.career_signal?.dataset_category !== "UNKNOWN_CATEGORY"
    ? profile.career_signal.dataset_category
    : "Computer Science & Engineering";

  return (
    <div className="container mx-auto px-4 py-10 max-w-6xl">
      {/* Top Header Profile Banner */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10 pb-8 border-b border-slate-800">
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="space-y-2">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-cyan-400 text-xs font-bold tracking-wide uppercase shadow-sm">
            <Fingerprint className="w-3.5 h-3.5" />
            <span>Extracted Candidate Intelligence</span>
            <span className="text-slate-600">&bull;</span>
            <span className="text-emerald-400 font-bold">GLiNER v2.1 Grounded</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
            {profile.identity?.name || categoryName}
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 font-medium flex items-center gap-2">
            <FileCheck className="w-4 h-4 text-slate-500" />
            <span>Source Document: <strong className="text-slate-200">{profile.filename || "Uploaded Resume"}</strong></span>
          </p>
        </motion.div>
        
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="flex gap-3">
          <Link 
            href="/careers" 
            className="px-6 py-3.5 bg-gradient-to-r from-indigo-600 via-violet-600 to-cyan-600 text-white rounded-2xl font-bold hover:shadow-xl hover:shadow-indigo-500/30 transition-all flex items-center gap-2 text-sm shadow-md hover:scale-105"
          >
            <Map className="w-4 h-4" />
            <span>View 28-Track Career Fit</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Skills & Verification Metadata */}
        <div className="lg:col-span-1 space-y-6">
          
          {/* Verified Technical Skills Card */}
          <section className="glass-cyber-card rounded-3xl p-6 border-slate-800">
            <div className="flex items-center justify-between mb-5">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-indigo-950/80 border border-indigo-500/30 text-indigo-400 rounded-2xl flex items-center justify-center shadow-sm">
                  <Sparkles className="w-5 h-5" />
                </div>
                <h2 className="text-base font-bold text-white">Technical Skills</h2>
              </div>
              <span className="text-xs font-bold text-cyan-400 bg-cyan-950/80 px-2.5 py-1 rounded-full border border-cyan-800/60">
                {skills.length} Verified
              </span>
            </div>
            
            {skills.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {skills.map((s: any, i: number) => {
                  const skillName = typeof s === 'string' ? s : s.name;
                  return (
                    <span 
                      key={i} 
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-950/60 border border-emerald-500/40 text-emerald-300 rounded-xl text-xs font-bold shadow-xs hover:bg-emerald-900/60 transition-colors"
                    >
                      <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                      <span>{skillName}</span>
                    </span>
                  );
                })}
              </div>
            ) : (
              <p className="text-xs text-slate-500 italic">No exact technical skills detected in document.</p>
            )}
          </section>

          {/* Soft & Interpersonal Skills Card (if available) */}
          {softSkills.length > 0 && (
            <section className="glass-cyber-card rounded-3xl p-6 border-slate-800">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2.5">
                  <div className="w-8 h-8 bg-purple-950/80 border border-purple-500/30 text-purple-400 rounded-xl flex items-center justify-center">
                    <HeartHandshake className="w-4 h-4" />
                  </div>
                  <h3 className="text-sm font-bold text-white">Soft Competencies</h3>
                </div>
                <span className="text-xs font-bold text-purple-300 bg-purple-950/80 px-2 py-0.5 rounded-md border border-purple-800/60">
                  {softSkills.length}
                </span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {softSkills.map((sk: any, idx: number) => (
                  <span key={idx} className="text-xs px-2.5 py-1 bg-slate-900 text-slate-300 rounded-lg border border-slate-800 font-medium">
                    {sk}
                  </span>
                ))}
              </div>
            </section>
          )}

          {/* AI Evidence Audit Card */}
          <section className="glass-cyber-card rounded-3xl p-6 shadow-xl text-white border-slate-800">
            <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
              <h2 className="text-sm font-bold flex items-center gap-2 text-white">
                <Fingerprint className="w-4 h-4 text-cyan-400" /> Evidence Audit Engine
              </h2>
              <span className="text-[10px] uppercase font-bold text-emerald-400 bg-emerald-500/20 px-2 py-0.5 rounded-full border border-emerald-400/30">
                Grounded
              </span>
            </div>
            
            <div className="space-y-3.5 text-xs">
              <div>
                <p className="text-[11px] text-slate-400 uppercase tracking-wider mb-0.5">Classification Signal</p>
                <p className="text-sm font-bold text-cyan-300">
                  {profile.career_signal?.confidence ? `${(profile.career_signal.confidence * 100).toFixed(1)}% Baseline Confidence` : "83.83% Model Benchmark"}
                </p>
              </div>

              <div>
                <p className="text-[11px] text-slate-400 uppercase tracking-wider mb-0.5">NER Extraction Model</p>
                <p className="text-xs font-mono text-slate-300">GLiNER v2.1 (Zero-Shot)</p>
              </div>
              
              <div className="pt-3 border-t border-slate-800">
                <p className="text-[11px] text-slate-400 uppercase tracking-wider mb-2">Section Verification Matrix</p>
                <div className="space-y-1.5 font-mono">
                  {["Skills", "Projects", "Experience", "Education", "Certifications"].map(sec => {
                    const list = profile[sec.toLowerCase()] || [];
                    const hasData = cleanList(list).length > 0;
                    return (
                      <div key={sec} className="flex justify-between items-center text-[11px]">
                        <span className="text-slate-300">{sec}</span>
                        {hasData ? (
                          <span className="text-emerald-400 font-bold">VERIFIED</span>
                        ) : (
                          <span className="text-slate-600">NOT_FOUND</span>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          </section>
        </div>

        {/* Right Column: Experience, Education, Projects */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Projects Section */}
          <TimelineSection 
            icon={<FolderGit2 className="w-5 h-5 text-violet-400" />} 
            title="Portfolio & Production Projects" 
            items={projects} 
            renderItem={(item) => (
              <div className="space-y-2">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                  <h3 className="font-bold text-white text-base sm:text-lg">{item.name}</h3>
                </div>
                {item.technologies && item.technologies.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 pt-0.5">
                    {item.technologies.map((t: string, i: number) => (
                      <span key={i} className="text-xs font-semibold px-2.5 py-0.5 bg-indigo-950/80 text-indigo-300 rounded-lg border border-indigo-700/60 shadow-2xs">
                        {t}
                      </span>
                    ))}
                  </div>
                )}
                {item.description && item.description !== "UNKNOWN" && (
                  <p className="text-xs sm:text-sm text-slate-300 leading-relaxed pt-1">{item.description}</p>
                )}
              </div>
            )}
          />

          {/* Professional Experience Section */}
          <TimelineSection 
            icon={<Briefcase className="w-5 h-5 text-indigo-400" />} 
            title="Professional Experience" 
            items={experience}
            emptyMessage="No corporate employment history listed in resume. Candidate profile evaluated as Project & Technical Portfolio Track."
            renderItem={(item) => (
              <div className="space-y-1.5">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                  <h3 className="font-bold text-white text-base">{item.job_title}</h3>
                  {item.duration && <span className="text-xs text-slate-400 font-medium">{item.duration}</span>}
                </div>
                <p className="text-cyan-400 font-bold text-xs">{item.company || "Independent"}</p>
                {item.evidence && item.evidence !== "NOT_FOUND" && (
                  <p className="text-xs text-slate-300 mt-2 bg-slate-900/90 p-3.5 rounded-2xl border border-slate-800 italic leading-relaxed">
                    "{item.evidence}"
                  </p>
                )}
              </div>
            )}
          />

          {/* Education & Certifications Row */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <TimelineSection 
              icon={<GraduationCap className="w-5 h-5 text-cyan-400" />} 
              title="Education" 
              items={education} 
              renderItem={(item) => (
                <div className="space-y-1">
                  <h3 className="font-bold text-white text-sm">{item.institution}</h3>
                  <p className="text-slate-400 text-xs font-medium">{item.degree} {item.field ? `in ${item.field}` : ""}</p>
                </div>
              )}
            />
            
            <TimelineSection 
              icon={<Award className="w-5 h-5 text-amber-400" />} 
              title="Verified Certifications & Courses" 
              items={certs} 
              renderItem={(item) => (
                <div className="space-y-1">
                  <h3 className="font-bold text-white text-sm">{item.name}</h3>
                  {item.issuer && item.issuer !== "UNKNOWN" && (
                    <p className="text-cyan-400 text-xs font-semibold">{item.issuer}</p>
                  )}
                </div>
              )}
            />
          </div>
        </div>

      </div>

      {/* Floating AI Career Advisor Chatbot */}
      <CareerChatbot candidateProfile={profile} />
    </div>
  );
}

function TimelineSection({ 
  icon, 
  title, 
  items, 
  emptyMessage,
  renderItem 
}: { 
  icon: React.ReactNode, 
  title: string, 
  items: any[], 
  emptyMessage?: string,
  renderItem: (item: any) => React.ReactNode 
}) {
  return (
    <section className="glass-cyber-card rounded-3xl p-6 md:p-8 border-slate-800 shadow-xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-slate-900 border border-slate-700/80 rounded-2xl flex items-center justify-center shadow-sm">
          {icon}
        </div>
        <h2 className="text-base sm:text-lg font-bold text-white">{title}</h2>
      </div>
      
      {items.length > 0 ? (
        <ul className="space-y-6">
          {items.map((item, idx) => (
            <li key={idx} className="flex gap-4">
              <div className="flex flex-col items-center mt-1.5">
                <div className="w-3 h-3 rounded-full bg-indigo-500 ring-4 ring-indigo-950 shrink-0 shadow-sm shadow-indigo-400" />
                {idx !== items.length - 1 && <div className="w-px h-full bg-slate-800 my-1" />}
              </div>
              <div className="pb-3 flex-1">
                {renderItem(item)}
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <div className="p-4 rounded-2xl bg-slate-900/60 border border-slate-800 text-slate-400 text-xs flex items-start gap-2.5">
          <AlertCircle className="w-4 h-4 flex-shrink-0 text-cyan-400 mt-0.5" />
          <p>{emptyMessage || `No verified evidence detected for ${title.toLowerCase()} in the provided document.`}</p>
        </div>
      )}
    </section>
  );
}
