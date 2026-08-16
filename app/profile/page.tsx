"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Briefcase, GraduationCap, Map, FolderGit2, Award, ChevronRight, Fingerprint, Sparkles, ServerCrash, CheckCircle2, AlertCircle } from "lucide-react";
import { motion } from "framer-motion";
import { useCandidate } from "@/lib/store/CandidateStore";

export default function ProfilePage() {
  const { profile, isHydrated } = useCandidate();
  if (!isHydrated) return <div className="p-24 text-center text-slate-400">Loading intelligence...</div>;

  if (!profile) {
    return (
      <div className="container mx-auto px-4 py-24 text-center max-w-lg">
        <div className="w-16 h-16 bg-red-50 text-red-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
          <ServerCrash className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Profile Not Found</h2>
        <p className="text-slate-500 mb-8">No profile data found. Please upload a resume first.</p>
        <Link href="/upload" className="px-6 py-3 bg-indigo-600 text-white rounded-full font-medium hover:bg-indigo-700 transition-colors">
          Upload Resume
        </Link>
      </div>
    );
  }

  // Helper to cleanly map arrays of objects that might contain UNKNOWN entries
  const cleanList = (arr: any) => {
    if (!Array.isArray(arr)) return [];
    return arr.filter(item => {
      if (typeof item === 'string') return item !== "UNKNOWN";
      if (typeof item === 'object') {
        // If it's a completely unknown object
        if (item.name === "UNKNOWN" || item.job_title === "UNKNOWN" || item.institution === "UNKNOWN") return false;
        return true;
      }
      return false;
    });
  };
  
  const skills = cleanList(profile.skills);
  const experience = cleanList(profile.experience);
  const education = cleanList(profile.education);
  const projects = cleanList(profile.projects);
  const certs = cleanList(profile.certifications);

  return (
    <div className="container mx-auto px-4 py-12 max-w-6xl">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }}>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-100 text-slate-600 text-xs font-semibold mb-4 tracking-wide uppercase">
            <Fingerprint className="w-3.5 h-3.5" />
            Candidate Intelligence
          </div>
          <h1 className="text-4xl font-extrabold text-slate-900 mb-2">
            {profile.career_signal?.dataset_category && profile.career_signal?.dataset_category !== "UNKNOWN_CATEGORY" 
              ? profile.career_signal.dataset_category 
              : "Career Profile"}
          </h1>
          <p className="text-slate-500">Source: {profile.filename}</p>
        </motion.div>
        
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="flex gap-3">
          <Link href="/careers" className="px-5 py-2.5 bg-white border border-slate-200 text-slate-700 rounded-full font-medium hover:bg-slate-50 transition-colors flex items-center gap-2">
            <Map className="w-4 h-4" /> Career Map
          </Link>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Skills & Evidence */}
        <div className="lg:col-span-1 space-y-8">
          <section className="bg-white rounded-3xl p-6 border border-slate-100 shadow-sm">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center">
                <Sparkles className="w-5 h-5" />
              </div>
              <h2 className="text-lg font-bold text-slate-900">Verified Skills</h2>
            </div>
            
            {skills.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {skills.map((s: any, i: number) => {
                  const skillName = typeof s === 'string' ? s : s.name;
                  return (
                    <span key={i} className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 border border-emerald-100 text-emerald-700 rounded-lg text-sm font-semibold">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      {skillName}
                    </span>
                  );
                })}
              </div>
            ) : (
              <p className="text-sm text-slate-400 italic">No exact skills extracted.</p>
            )}
          </section>

          <section className="bg-slate-900 rounded-3xl p-6 shadow-sm text-white">
            <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
              <Fingerprint className="w-5 h-5 text-indigo-400" /> Evidence Engine
            </h2>
            <div className="space-y-4">
              <div>
                <p className="text-xs text-slate-400 uppercase tracking-wider mb-1">Extraction Method</p>
                <p className="text-sm font-medium text-slate-200">Multi-Stage LLM Pipeline</p>
              </div>
              <div>
                <p className="text-xs text-slate-400 uppercase tracking-wider mb-1">Confidence</p>
                <div className="inline-flex items-center gap-1.5 px-2 py-1 rounded-md bg-emerald-500/20 text-emerald-400 text-xs font-semibold">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  EVIDENCE-BACKED
                </div>
              </div>
              
              <div className="pt-4 border-t border-slate-700">
                <p className="text-xs text-slate-400 uppercase tracking-wider mb-2">Anti-Hallucination Checks</p>
                <div className="space-y-2">
                   {["Projects", "Experience", "Education"].map(sec => {
                      const list = profile[sec.toLowerCase()] || [];
                      const hasData = cleanList(list).length > 0;
                      return (
                        <div key={sec} className="flex justify-between items-center text-xs">
                          <span className="text-slate-300">{sec}</span>
                          {hasData ? (
                            <span className="text-emerald-400 font-mono">FOUND</span>
                          ) : (
                            <span className="text-amber-400 font-mono">NOT_FOUND</span>
                          )}
                        </div>
                      )
                   })}
                </div>
              </div>
            </div>
          </section>
        </div>

        {/* Right Column: Experience, Education, Projects */}
        <div className="lg:col-span-2 space-y-8">
          <TimelineSection 
            icon={<Briefcase />} 
            title="Professional Experience" 
            items={experience}
            renderItem={(item) => (
              <div>
                <h3 className="font-bold text-slate-900 text-lg">{item.job_title}</h3>
                <p className="text-indigo-600 font-semibold mb-1">{item.company}</p>
                {item.evidence && item.evidence !== "NOT_FOUND" && (
                  <p className="text-sm text-slate-600 mt-2 bg-slate-50 p-3 rounded-lg border border-slate-100 italic leading-relaxed">
                    "{item.evidence}"
                  </p>
                )}
              </div>
            )}
          />
          
          <TimelineSection 
            icon={<FolderGit2 />} 
            title="Projects" 
            items={projects} 
            renderItem={(item) => (
              <div>
                <h3 className="font-bold text-slate-900 text-lg">{item.name}</h3>
                {item.technologies && item.technologies.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {item.technologies.map((t: string, i: number) => (
                      <span key={i} className="text-xs px-2 py-0.5 bg-slate-100 text-slate-600 rounded">
                        {t}
                      </span>
                    ))}
                  </div>
                )}
                {item.description && item.description !== "UNKNOWN" && (
                   <p className="text-sm text-slate-600 mt-2">{item.description}</p>
                )}
                {item.evidence && item.evidence !== "NOT_FOUND" && (
                  <p className="text-sm text-slate-500 mt-2 bg-slate-50 p-3 rounded-lg border border-slate-100 italic">
                    Evidence: "{item.evidence}"
                  </p>
                )}
              </div>
            )}
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <TimelineSection 
              icon={<GraduationCap />} 
              title="Education" 
              items={education} 
              renderItem={(item) => (
                <div>
                  <h3 className="font-bold text-slate-900">{item.institution}</h3>
                  <p className="text-slate-600 text-sm">{item.degree}</p>
                </div>
              )}
            />
            
            <TimelineSection 
              icon={<Award />} 
              title="Certifications" 
              items={certs} 
              renderItem={(item) => (
                <div>
                  <h3 className="font-bold text-slate-900">{item.name}</h3>
                  {item.issuer && item.issuer !== "UNKNOWN" && (
                    <p className="text-slate-600 text-sm">{item.issuer}</p>
                  )}
                </div>
              )}
            />
          </div>
        </div>

      </div>
    </div>
  );
}

function TimelineSection({ icon, title, items, renderItem }: { icon: React.ReactNode, title: string, items: any[], renderItem: (item: any) => React.ReactNode }) {
  return (
    <section className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center">
          {icon}
        </div>
        <h2 className="text-xl font-bold text-slate-900">{title}</h2>
      </div>
      
      {items.length > 0 ? (
        <ul className="space-y-6">
          {items.map((item, idx) => (
            <li key={idx} className="flex gap-4">
              <div className="flex flex-col items-center mt-1.5">
                <div className="w-3 h-3 rounded-full bg-indigo-600 ring-4 ring-indigo-50" />
                {idx !== items.length - 1 && <div className="w-px h-full bg-slate-100 my-1" />}
              </div>
              <div className="pb-4 flex-1">
                {renderItem(item)}
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <div className="p-4 rounded-xl bg-amber-50 border border-amber-100 text-amber-800 text-sm flex items-start gap-2">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <p>No verified evidence found for {title.toLowerCase()} in the provided document.</p>
        </div>
      )}
    </section>
  );
}
