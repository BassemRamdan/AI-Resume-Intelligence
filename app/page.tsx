"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Briefcase, Compass, Map, FileSearch } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col min-h-[calc(100vh-4rem)] bg-white overflow-hidden">
      {/* Background gradients */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-indigo-50 via-white to-white -z-10" />
      
      <div className="flex-1 container mx-auto px-4 flex flex-col justify-center items-center text-center py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-4xl"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 text-indigo-600 text-sm font-medium mb-8 border border-indigo-100">
            <span className="flex h-2 w-2 rounded-full bg-indigo-600"></span>
            CareerLens AI V2
          </div>
          
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight text-slate-900 mb-6 leading-[1.1]">
            Understand where you are. <br className="hidden md:block" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-600">
              Discover where you fit.
            </span>
          </h1>
          
          <p className="text-xl text-slate-600 mb-10 max-w-2xl mx-auto leading-relaxed">
            Stop guessing your next career move. Upload your resume to instantly generate an AI-powered evidence-based career map, discover your true market value, and get a personalized learning roadmap.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link 
              href="/upload" 
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-slate-900 text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-slate-800 transition-all hover:scale-105 active:scale-95 shadow-xl shadow-slate-900/10"
            >
              Analyze My Resume <ArrowRight className="w-5 h-5" />
            </Link>
            <Link 
              href="/careers" 
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-white text-slate-900 border-2 border-slate-200 px-8 py-4 rounded-full font-semibold text-lg hover:border-slate-300 hover:bg-slate-50 transition-colors"
            >
              Explore Career Paths
            </Link>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          className="mt-24 grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl"
        >
          <FeatureCard 
            icon={<FileSearch className="w-6 h-6 text-indigo-600" />}
            title="Candidate Intelligence"
            description="Deep extraction of your skills and experience using deterministic ML models."
          />
          <FeatureCard 
            icon={<Compass className="w-6 h-6 text-indigo-600" />}
            title="Career Discovery"
            description="Visualize your readiness for adjacent and alternative career roles."
          />
        </motion.div>

        {/* System Architecture Explanation */}
        <motion.div 
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.4 }}
          className="mt-32 w-full max-w-5xl text-left"
        >
          <h2 className="text-3xl font-bold text-slate-900 mb-8 text-center">How The Hybrid Pipeline Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-slate-50 rounded-3xl p-8 border border-slate-100">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-indigo-100 text-indigo-700 rounded-lg flex items-center justify-center font-bold">1</div>
                <h3 className="text-xl font-bold text-slate-900">Information Extraction (Groq & GLiNER)</h3>
              </div>
              <p className="text-slate-600 leading-relaxed">
                When you upload a CV, we use <strong>PyMuPDF</strong> to extract the text structure. Then, we use a specialized NLP model called <strong>GLiNER</strong> to find entities (like job titles and universities). Finally, we pass the raw text to <strong>Groq (LLaMA-3)</strong>. Groq acts as a smart parser to clean and structure the data into a strict JSON format (Skills, Experience, Projects). We force the LLM to provide exact evidence from the CV to prevent hallucinations.
              </p>
            </div>
            
            <div className="bg-slate-50 rounded-3xl p-8 border border-slate-100">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-indigo-100 text-indigo-700 rounded-lg flex items-center justify-center font-bold">2</div>
                <h3 className="text-xl font-bold text-slate-900">Career Classification (DistilBERT)</h3>
              </div>
              <p className="text-slate-600 leading-relaxed">
                While Groq extracts your details, the raw text is also sent to our custom fine-tuned <strong>DistilBERT</strong> model. This model has been trained on thousands of resumes to predict your overarching career category (e.g., Data Science, Software Engineering) with high accuracy, establishing your primary professional identity.
              </p>
            </div>

            <div className="bg-slate-50 rounded-3xl p-8 border border-slate-100 md:col-span-2">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 bg-indigo-100 text-indigo-700 rounded-lg flex items-center justify-center font-bold">3</div>
                <h3 className="text-xl font-bold text-slate-900">Semantic Matching Engine (SentenceTransformers)</h3>
              </div>
              <p className="text-slate-600 leading-relaxed">
                Once we have your structured profile, we use <strong>all-MiniLM-L6-v2</strong> to convert your skills, projects, and titles into mathematical vectors (embeddings). We calculate a multi-factor score (Skill Match, Project Match, Title Fit) by comparing your embeddings against our Career Taxonomy prototypes. Finally, we run K-Nearest Neighbors (KNN) to find other resumes similar to yours, giving you a completely explainable and precise career map.
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
  return (
    <div className="text-left p-6 rounded-2xl bg-white border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
      <div className="w-12 h-12 rounded-xl bg-indigo-50 flex items-center justify-center mb-4">
        {icon}
      </div>
      <h3 className="font-semibold text-slate-900 mb-2">{title}</h3>
      <p className="text-sm text-slate-500 leading-relaxed">{description}</p>
    </div>
  );
}
