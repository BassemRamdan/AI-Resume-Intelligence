import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import { CandidateProvider } from "@/lib/store/CandidateStore";
import { Sparkles, BrainCircuit, Compass, FileText, UserCheck, Layers, Terminal } from "lucide-react";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "CareerLens AI — AI-Driven Resume Intelligence & Career Recommendation",
  description: "Transform unstructured resume PDFs into structured candidate profiles, deterministic career fit rankings, and personalized 3-phase roadmaps.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body className="min-h-full flex flex-col bg-[#050814] text-slate-100 font-sans relative overflow-x-hidden selection:bg-indigo-500 selection:text-white">
        
        {/* Dynamic Multi-Layer Cyber Aurora Background */}
        <div className="fixed inset-0 pointer-events-none -z-10 overflow-hidden">
          {/* Tech Grid Pattern */}
          <div className="absolute inset-0 bg-grid-cyber opacity-70" />
          
          {/* Subtle Dot Matrix Accent */}
          <div className="absolute inset-0 bg-dots-cyber opacity-40" />
          
          {/* Orb 1: Electric Ultra-Indigo (Top-Left / Center) */}
          <div className="absolute -top-40 left-1/4 w-[800px] h-[600px] bg-gradient-to-tr from-indigo-600/30 via-indigo-500/20 to-transparent rounded-full blur-[140px] animate-aurora-1" />
          
          {/* Orb 2: Deep Violet / Purple Neon (Middle / Right) */}
          <div className="absolute top-[350px] -right-32 w-[700px] h-[700px] bg-gradient-to-br from-purple-600/25 via-violet-500/20 to-transparent rounded-full blur-[150px] animate-aurora-2" />
          
          {/* Orb 3: Cyber Cyan (Bottom / Left) */}
          <div className="absolute top-[900px] -left-32 w-[750px] h-[650px] bg-gradient-to-tr from-cyan-500/25 via-teal-400/15 to-transparent rounded-full blur-[130px] animate-aurora-3" />
        </div>

        <CandidateProvider>
          {/* Sticky Cyber-Glass Header */}
          <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/70 backdrop-blur-2xl transition-all shadow-lg shadow-black/40">
            <div className="container mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
              
              {/* Brand Logo with 3-Color Glow Icon */}
              <Link href="/" className="flex items-center gap-3 group">
                <div className="h-10 w-10 rounded-2xl bg-gradient-to-tr from-indigo-500 via-violet-500 to-cyan-400 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30 group-hover:scale-105 group-hover:shadow-indigo-500/50 transition-all p-[1px]">
                  <div className="w-full h-full rounded-[15px] bg-slate-950 flex items-center justify-center">
                    <BrainCircuit className="w-5 h-5 text-cyan-400" />
                  </div>
                </div>
                <div className="flex flex-col">
                  <div className="flex items-center gap-1.5">
                    <span className="text-base font-black tracking-tight text-white">
                      CareerLens
                    </span>
                    <span className="text-xs font-black px-1.5 py-0.5 rounded-md bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-xs">
                      AI
                    </span>
                  </div>
                  <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider hidden sm:block">
                    Resume Intelligence &bull; 6 Models
                  </span>
                </div>
              </Link>

              {/* Navigation Links */}
              <nav className="hidden md:flex items-center gap-1 text-xs font-bold text-slate-300 tracking-wide">
                <Link 
                  href="/" 
                  className="px-3.5 py-2 rounded-xl hover:text-white hover:bg-white/5 transition-all"
                >
                  Overview
                </Link>
                <Link 
                  href="/upload" 
                  className="px-3.5 py-2 rounded-xl hover:text-white hover:bg-white/5 transition-all flex items-center gap-1.5"
                >
                  <FileText className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Analyze Resume</span>
                </Link>
                <Link 
                  href="/profile" 
                  className="px-3.5 py-2 rounded-xl hover:text-white hover:bg-white/5 transition-all flex items-center gap-1.5"
                >
                  <UserCheck className="w-3.5 h-3.5 text-violet-400" />
                  <span>Candidate Profile</span>
                </Link>
                <Link 
                  href="/careers" 
                  className="px-3.5 py-2 rounded-xl hover:text-white hover:bg-white/5 transition-all flex items-center gap-1.5"
                >
                  <Compass className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Career Map</span>
                </Link>
              </nav>

              {/* Action Button with 3-Color Gradient Rim */}
              <div className="flex items-center gap-3">
                <Link 
                  href="/upload" 
                  className="relative group inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-indigo-500 via-violet-500 to-cyan-400 p-[1px] shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40 hover:scale-105 active:scale-95 transition-all"
                >
                  <div className="flex items-center gap-2 bg-slate-950 px-4 py-2 rounded-[11px] text-xs font-bold text-white group-hover:bg-slate-900 transition-colors">
                    <Sparkles className="w-3.5 h-3.5 text-cyan-300 animate-pulse" />
                    <span>Upload Resume</span>
                  </div>
                </Link>
              </div>

            </div>
          </header>

          {/* Main Body */}
          <main className="flex-1 relative z-10">
            {children}
          </main>
        </CandidateProvider>
      </body>
    </html>
  );
}
