"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { 
  ArrowRight, 
  Sparkles, 
  Cpu, 
  ShieldCheck, 
  Map, 
  Layers, 
  CheckCircle2, 
  XCircle, 
  Activity, 
  BrainCircuit, 
  Terminal, 
  FileText,
  Compass,
  Zap,
  Lock,
  ChevronRight,
  TrendingUp,
  FileCheck2,
  Users
} from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen overflow-hidden selection:bg-indigo-500 selection:text-white">
      
      {/* Hero Section */}
      <section className="relative pt-16 pb-14 md:pt-24 md:pb-20 px-4 container mx-auto max-w-6xl text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="space-y-6 max-w-4xl mx-auto"
        >
          {/* Animated 3-Color Glow Badge */}
          <div className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-slate-900/90 border border-slate-800 shadow-lg shadow-black/40 text-slate-200 text-xs md:text-sm font-semibold tracking-wide backdrop-blur-xl">
            <span className="flex h-2.5 w-2.5 rounded-full bg-emerald-400 animate-pulse shadow-sm shadow-emerald-400" />
            <span className="font-extrabold text-gradient-neon">AI-Driven Resume Intelligence & Deterministic Mapping</span>
            <span className="text-slate-600">|</span>
            <span className="text-cyan-400 font-bold">6-Model Architecture</span>
          </div>

          {/* Main Title with 3-Color Dynamic Gradient */}
          <h1 className="text-4xl sm:text-6xl md:text-7xl font-black tracking-tight text-white leading-[1.12]">
            Transform Unstructured Resumes Into{" "}
            <span className="text-gradient-tri block sm:inline">
              Verifiable Career Intelligence
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-base sm:text-lg md:text-xl text-slate-300 max-w-2xl mx-auto leading-relaxed font-normal">
            No keyword-stuffing exploits. No LLM scoring hallucinations. CareerLens AI coordinates <strong>6 specialized ML models</strong> and deterministic 6-signal mathematics to rank candidate compatibility and construct personalized 3-phase roadmaps.
          </p>

          {/* Action CTAs with 3-Color Glowing Gradients */}
          <div className="pt-3 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              href="/upload"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-3 bg-gradient-to-r from-indigo-600 via-violet-600 to-cyan-600 text-white px-8 py-4 rounded-2xl font-black text-base shadow-xl shadow-indigo-500/30 hover:shadow-indigo-500/50 hover:scale-[1.03] active:scale-[0.98] transition-all"
            >
              <span>Analyze Resume PDF</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="/careers"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 bg-slate-900/90 text-white border border-slate-700/80 px-8 py-4 rounded-2xl font-bold text-base hover:bg-slate-800 hover:border-indigo-400 shadow-md transition-all hover:scale-[1.02]"
            >
              <Compass className="w-5 h-5 text-cyan-400" />
              <span>Explore 28 Career Tracks</span>
            </Link>
          </div>
        </motion.div>

        {/* Live Empirical Metrics Strip with 3-Color Dark Glass Cards */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="mt-14 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto"
        >
          <div className="p-5 rounded-2xl glass-cyber-card glass-cyber-card-indigo text-center">
            <div className="text-3xl md:text-4xl font-black text-indigo-400 tracking-tight">83.83%</div>
            <div className="text-xs uppercase tracking-wider font-bold text-slate-400 mt-1">Transformer Accuracy</div>
          </div>
          <div className="p-5 rounded-2xl glass-cyber-card glass-cyber-card-violet text-center">
            <div className="text-3xl md:text-4xl font-black text-violet-400 tracking-tight">6-Signal</div>
            <div className="text-xs uppercase tracking-wider font-bold text-slate-400 mt-1">Deterministic Formula</div>
          </div>
          <div className="p-5 rounded-2xl glass-cyber-card glass-cyber-card-cyan text-center">
            <div className="text-3xl md:text-4xl font-black text-cyan-400 tracking-tight">2,466</div>
            <div className="text-xs uppercase tracking-wider font-bold text-slate-400 mt-1">Benchmarked Resumes</div>
          </div>
          <div className="p-5 rounded-2xl glass-cyber-card text-center border-t-2 border-t-emerald-500">
            <div className="text-3xl md:text-4xl font-black text-emerald-400 tracking-tight">120B LLM</div>
            <div className="text-xs uppercase tracking-wider font-bold text-slate-400 mt-1">Groq RAG Advisory</div>
          </div>
        </motion.div>
      </section>

      {/* 3-Color Engineered AI Ecosystem Showcase */}
      <section className="py-16 px-4 container mx-auto max-w-6xl">
        <div className="text-center max-w-2xl mx-auto mb-14 space-y-2.5">
          <div className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-cyan-400 text-xs font-bold uppercase tracking-wider">
            <Cpu className="w-3.5 h-3.5 text-cyan-400" /> Multi-Model Architecture
          </div>
          <h2 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
            How CareerLens AI Achieves 0% Scoring Hallucination
          </h2>
          <p className="text-slate-400 text-sm sm:text-base">
            We strictly decouple deterministic factual scoring from generative natural language advisory.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8">
          {/* Card 1: Electric Indigo Theme */}
          <motion.div 
            whileHover={{ y: -6 }}
            className="p-8 rounded-3xl glass-cyber-card glass-cyber-card-indigo flex flex-col justify-between"
          >
            <div>
              <div className="w-12 h-12 rounded-2xl bg-indigo-950/80 border border-indigo-500/30 flex items-center justify-center text-indigo-400 mb-6 font-bold shadow-xs">
                <FileText className="w-6 h-6" />
              </div>
              <span className="text-[11px] font-extrabold uppercase tracking-wider text-indigo-300 bg-indigo-950/80 px-2.5 py-1 rounded-md border border-indigo-800/60">
                Extraction Layer
              </span>
              <h3 className="text-xl font-black text-white mt-3 mb-2">GLiNER Zero-Shot & Ontology</h3>
              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                PyMuPDF extracts layout structure while <code>urchade/gliner_multi-v2.1</code> identifies skills, projects, and credentials without regex brittleness. A 117-entity canonical ontology normalizes variations.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-800 text-xs font-semibold text-slate-400 flex items-center justify-between">
              <span>Model: GLiNER v2.1</span>
              <span className="text-emerald-400 font-bold">Zero-Shot NER</span>
            </div>
          </motion.div>

          {/* Card 2: Royal Violet Theme */}
          <motion.div 
            whileHover={{ y: -6 }}
            className="p-8 rounded-3xl glass-cyber-card glass-cyber-card-violet flex flex-col justify-between relative overflow-hidden"
          >
            <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-bl from-purple-500/15 to-transparent rounded-bl-full pointer-events-none" />
            <div>
              <div className="w-12 h-12 rounded-2xl bg-violet-600 text-white flex items-center justify-center mb-6 font-bold shadow-lg shadow-purple-500/30">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <span className="text-[11px] font-extrabold uppercase tracking-wider text-violet-300 bg-purple-950/80 px-2.5 py-1 rounded-md border border-purple-800/60">
                Deterministic Core
              </span>
              <h3 className="text-xl font-black text-white mt-3 mb-2">6-Signal Career Fit Engine</h3>
              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                Evaluates candidate profile against 28 specialized tracks using a strict weighted formula: 35% Skills, 20% Projects, 20% Prototype Cosine, 10% Edu, 10% Exp, 5% Classifier. Protected by an Anti-Hallucination Relevance Gate.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-800 text-xs font-semibold text-slate-400 flex items-center justify-between">
              <span>Formula: lib/career/engine.py</span>
              <span className="text-violet-400 font-bold">100% Deterministic</span>
            </div>
          </motion.div>

          {/* Card 3: Cyber Cyan Theme */}
          <motion.div 
            whileHover={{ y: -6 }}
            className="p-8 rounded-3xl glass-cyber-card glass-cyber-card-cyan flex flex-col justify-between"
          >
            <div>
              <div className="w-12 h-12 rounded-2xl bg-cyan-950/80 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mb-6 font-bold shadow-xs">
                <BrainCircuit className="w-6 h-6" />
              </div>
              <span className="text-[11px] font-extrabold uppercase tracking-wider text-cyan-300 bg-cyan-950/80 px-2.5 py-1 rounded-md border border-cyan-800/60">
                Advisory Layer
              </span>
              <h3 className="text-xl font-black text-white mt-3 mb-2">Groq 120B & Dense RAG</h3>
              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                Groq flagship 120B model and dense semantic RAG retrieve domain milestones from a 24-domain expert knowledge base to explain fit scores and deliver custom 3-phase transition roadmaps.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-slate-800 text-xs font-semibold text-slate-400 flex items-center justify-between">
              <span>Engine: Groq 120B + RAG</span>
              <span className="text-cyan-400 font-bold">Grounded Output</span>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Comparison: Why Traditional Tools Fail */}
      <section className="py-16 px-4 container mx-auto max-w-5xl">
        <div className="p-8 sm:p-12 rounded-3xl bg-slate-950/90 text-white shadow-2xl relative overflow-hidden border border-slate-800">
          <div className="absolute -right-20 -bottom-20 w-80 h-80 bg-gradient-to-tr from-indigo-600/30 via-violet-600/20 to-cyan-500/20 rounded-full blur-3xl pointer-events-none" />
          
          <div className="max-w-2xl mb-8">
            <span className="text-xs font-bold uppercase tracking-widest text-cyan-400">Industry Paradigm Shift</span>
            <h2 className="text-2xl sm:text-4xl font-black mt-2 mb-3 tracking-tight text-white">
              Why Keyword Parsers & Raw LLMs Fall Short
            </h2>
            <p className="text-slate-400 text-xs sm:text-sm">
              Comparing traditional approaches with CareerLens AI's hybrid deterministic intelligence.
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs sm:text-sm border-collapse">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 uppercase tracking-wider text-[11px]">
                  <th className="pb-4 font-bold">Capability</th>
                  <th className="pb-4 font-bold text-rose-400">Traditional ATS</th>
                  <th className="pb-4 font-bold text-amber-400">Pure Commercial LLMs</th>
                  <th className="pb-4 font-bold text-emerald-400">CareerLens AI</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-medium">
                <tr>
                  <td className="py-4 font-semibold text-slate-200">Scoring Reproducibility</td>
                  <td className="py-4 text-slate-400">Static regex matches</td>
                  <td className="py-4 text-rose-300 flex items-center gap-1.5"><XCircle className="w-4 h-4" /> Fluctuates per prompt</td>
                  <td className="py-4 text-emerald-300 font-bold flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4" /> 100% Deterministic Math</td>
                </tr>
                <tr>
                  <td className="py-4 font-semibold text-slate-200">Hallucination Risk</td>
                  <td className="py-4 text-slate-400">High false negatives</td>
                  <td className="py-4 text-rose-300 flex items-center gap-1.5"><XCircle className="w-4 h-4" /> High (Fabricates skills)</td>
                  <td className="py-4 text-emerald-300 font-bold flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4" /> 0% (Relevance Gate)</td>
                </tr>
                <tr>
                  <td className="py-4 font-semibold text-slate-200">Audit Trail & Evidence</td>
                  <td className="py-4 text-slate-400">None</td>
                  <td className="py-4 text-slate-400">Unverifiable black-box</td>
                  <td className="py-4 text-emerald-300 font-bold flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4" /> Verbatim JSON Evidence</td>
                </tr>
                <tr>
                  <td className="py-4 font-semibold text-slate-200">Actionable 3-Phase Roadmap</td>
                  <td className="py-4 text-slate-400">None</td>
                  <td className="py-4 text-slate-400">Generic unstructured text</td>
                  <td className="py-4 text-emerald-300 font-bold flex items-center gap-1.5"><CheckCircle2 className="w-4 h-4" /> Dense Semantic RAG</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* Call to Action Footer Banner */}
      <section className="py-12 px-4 container mx-auto max-w-4xl text-center">
        <div className="p-8 sm:p-12 rounded-3xl glass-cyber-card border border-indigo-500/30 shadow-2xl text-center relative overflow-hidden">
          <div className="absolute -top-24 -left-24 w-48 h-48 bg-gradient-to-tr from-indigo-500/30 to-cyan-500/30 rounded-full blur-2xl pointer-events-none" />
          <h2 className="text-2xl sm:text-3xl font-black text-white mb-3 tracking-tight">
            Ready to Experience Evidence-Based Career Intelligence?
          </h2>
          <p className="text-slate-300 text-xs sm:text-base max-w-xl mx-auto mb-8 leading-relaxed">
            Upload your resume to receive an instantaneous breakdown of your skills, domain classification, KNN peer benchmarks, and customized career roadmaps.
          </p>
          <Link
            href="/upload"
            className="inline-flex items-center gap-2.5 bg-gradient-to-r from-indigo-600 via-violet-600 to-cyan-600 text-white px-8 py-4 rounded-2xl font-black hover:opacity-95 shadow-xl shadow-indigo-500/30 hover:scale-105 active:scale-95 transition-all text-sm sm:text-base"
          >
            <span>Start Resume Analysis</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto border-t border-slate-800/80 bg-slate-950/80 backdrop-blur py-8 px-4 text-center text-xs text-slate-400">
        <div className="container mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 max-w-6xl">
          <div className="flex items-center gap-2 font-bold text-white text-sm">
            <div className="w-6 h-6 rounded-lg bg-gradient-to-tr from-indigo-600 to-cyan-500 flex items-center justify-center text-white text-xs font-bold">CL</div>
            <span>CareerLens AI</span>
          </div>
          <p>
            AI-Driven Resume Intelligence & Career Recommendation System &bull; Powered by PyMuPDF, GLiNER, DeBERTa, SentenceTransformers & Groq 120B
          </p>
          <div className="flex gap-4 font-semibold text-slate-400">
            <Link href="/upload" className="hover:text-cyan-400 transition-colors">Upload</Link>
            <Link href="/careers" className="hover:text-cyan-400 transition-colors">Career Map</Link>
            <Link href="/profile" className="hover:text-cyan-400 transition-colors">Profile</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
