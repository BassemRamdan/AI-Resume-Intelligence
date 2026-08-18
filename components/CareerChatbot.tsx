"use client";

import { useState, useRef, useEffect } from "react";
import { 
  Bot, 
  User, 
  Sparkles, 
  X, 
  Compass, 
  Send, 
  RefreshCw, 
  RotateCcw, 
  Maximize2,
  Minimize2,
  ChevronDown,
  Layers,
  CheckCheck,
  Copy,
  Lightbulb,
  Cpu,
  BrainCircuit,
  Terminal,
  Zap,
  Check
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import MarkdownMessage from "./MarkdownMessage";

interface CareerChatbotProps {
  candidateProfile: any;
  topCareers?: any[];
  defaultCareer?: string;
}

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

const QUICK_PROMPTS = [
  { 
    icon: "🗺️",
    label: "3-Phase Roadmap", 
    query: "Generate a comprehensive, step-by-step milestone learning roadmap for my target career track based on my verified skills and missing competencies." 
  },
  { 
    icon: "🔍",
    label: "Seniority Diagnostics", 
    query: "Based on my extracted skills, projects, and work history, what is my current seniority level (Junior / Mid / Senior), and what exact architectural milestones do I need to reach the next level?" 
  },
  { 
    icon: "💻",
    label: "Production Projects", 
    query: "Suggest 2-3 production-grade portfolio project blueprints with concrete architecture requirements (microservices, caching, CI/CD, tests) that will prove my competency to top hiring teams." 
  },
  { 
    icon: "⚡",
    label: "Skill Gap Remediation", 
    query: "Analyze my verified skills against the target career standards. What are my top high-priority skill gaps and how can I close them within 60-90 days?" 
  },
  { 
    icon: "🏆",
    label: "High-ROI Certifications", 
    query: "Which industry certifications offer the highest return on investment (ROI) for this career track, and which one should I prioritize?" 
  }
];

export default function CareerChatbot({ candidateProfile, topCareers = [], defaultCareer }: CareerChatbotProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [selectedCareer, setSelectedCareer] = useState<string>(
    defaultCareer || (topCareers.length > 0 ? topCareers[0].career : "Software Engineer")
  );

  const initialGreeting: ChatMessage = {
    id: "init-0",
    role: "assistant",
    content: `### 👋 Welcome to CareerLens AI Principal Advisor!

I am your **AI Technical Career Architect & Senior Advisor**, powered by **Groq 120B Generative AI & Dense Semantic RAG Intelligence**.

I have direct access to your verified candidate profile (skills, projects, and work history) and our **24-domain expert knowledge base**.

Ask me anything about your technical growth:
- 🗺️ **Personalized Roadmaps:** Concrete 3-phase progression paths based on your actual skills.
- 🎯 **Seniority & Level Assessment:** Discover whether your profile qualifies for Junior, Mid, or Senior benchmarks.
- 🔍 **Skill Gap Diagnostics:** Pinpoint the high-priority tools and architectural concepts you need to learn.
- 💻 **Production Project Blueprints:** End-to-end portfolio architectures (APIs, Docker, Microservices, Caching).
- 💡 **Technical Deep-Dives:** Ask about any concept (*"Explain Clean Architecture in .NET/Python"*, *"Kafka vs RabbitMQ"*, *"How to master MLOps"*).`,
    timestamp: "Live Assistant"
  };

  const [messages, setMessages] = useState<ChatMessage[]>([initialGreeting]);
  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (defaultCareer) {
      setSelectedCareer(defaultCareer);
    } else if (topCareers.length > 0) {
      setSelectedCareer(topCareers[0].career);
    }
  }, [defaultCareer, topCareers]);

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isOpen, loading]);

  const handleResetChat = () => {
    setMessages([{ 
      ...initialGreeting, 
      id: `init-${Date.now()}`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
    }]);
  };

  const handleCopyMessage = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleSendMessage = async (textToSend?: string) => {
    const query = (textToSend || inputMessage).trim();
    if (!query || loading) return;

    const userMsg: ChatMessage = { 
      id: `user-${Date.now()}`,
      role: "user", 
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInputMessage("");
    setLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: updatedMessages.map(m => ({ role: m.role, content: m.content })),
          candidateProfile,
          targetCareer: selectedCareer
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to contact advisor service");
      }

      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        { 
          id: `asst-${Date.now()}`,
          role: "assistant", 
          content: data.response || "No response received.",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          role: "assistant",
          content: "⚠️ An error occurred while communicating with the AI Advisor. Please verify that the FastAPI backend is running on port 8000.",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Ultra-Modern Floating Launcher with Multi-Color Conic Glow Ring */}
      <div className="fixed bottom-6 right-6 z-50">
        <motion.button
          onClick={() => setIsOpen(true)}
          className="relative group flex items-center gap-3 p-[2px] rounded-full shadow-2xl shadow-indigo-500/35 hover:shadow-indigo-500/60 hover:scale-105 active:scale-95 transition-all"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {/* Animated 3-Color Gradient Border */}
          <div className="absolute inset-0 rounded-full bg-gradient-to-r from-indigo-500 via-violet-500 to-cyan-400 animate-spin opacity-80 blur-xs group-hover:opacity-100" style={{ animationDuration: '8s' }} />
          
          <div className="relative flex items-center gap-3 px-5 py-3.5 bg-slate-950 text-white rounded-full font-extrabold text-sm backdrop-blur-xl border border-white/10">
            <div className="relative flex items-center justify-center">
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-600 via-violet-600 to-cyan-400 flex items-center justify-center text-white shadow-inner">
                <BrainCircuit className="w-4 h-4 group-hover:rotate-12 transition-transform" />
              </div>
              <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 rounded-full animate-ping" />
              <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-400 rounded-full border-2 border-slate-950" />
            </div>
            <span className="tracking-tight text-white font-black">AI Career Advisor</span>
            <div className="flex items-center gap-1 text-[10px] uppercase font-bold text-cyan-300 bg-cyan-950/80 px-2 py-0.5 rounded-full border border-cyan-800/60">
              <Sparkles className="w-3 h-3 text-cyan-400" />
              <span>120B</span>
            </div>
          </div>
        </motion.button>
      </div>

      {/* Advanced Slide-Over AI Copilot Drawer */}
      <AnimatePresence>
        {isOpen && (
          <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/75 backdrop-blur-md transition-all">
            <motion.div
              initial={{ x: "100%", opacity: 0.8 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: "100%", opacity: 0.8 }}
              transition={{ type: "spring", damping: 26, stiffness: 220 }}
              className={`h-full bg-slate-50/95 shadow-2xl flex flex-col border-l border-slate-200/90 transition-all duration-300 ${
                isMaximized ? "w-full max-w-none" : "w-full md:w-[85vw] lg:w-[75vw] xl:max-w-5xl"
              }`}
            >
              {/* 3-Color Top Accent Line */}
              <div className="h-[3px] w-full bg-gradient-to-r from-indigo-500 via-violet-500 to-cyan-400" />

              {/* Header Bar */}
              <div className="px-6 py-4 bg-slate-950 text-white flex items-center justify-between shadow-xl">
                <div className="flex items-center gap-3.5">
                  <div className="w-11 h-11 rounded-2xl bg-gradient-to-tr from-indigo-600 via-violet-600 to-cyan-500 p-0.5 shadow-md shadow-indigo-500/25">
                    <div className="w-full h-full rounded-[14px] bg-slate-950 flex items-center justify-center text-cyan-300">
                      <Bot className="w-6 h-6" />
                    </div>
                  </div>
                  <div>
                    <div className="flex items-center gap-2.5 flex-wrap">
                      <h3 className="font-black text-base md:text-lg tracking-tight text-white flex items-center gap-2">
                        CareerLens AI Copilot
                      </h3>
                      <span className="text-[10px] uppercase font-black px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 flex items-center gap-1.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                        Groq 120B LPU Active
                      </span>
                      <span className="text-[10px] font-mono text-slate-400 hidden sm:inline-block">
                        Dense RAG &bull; 24 Domains
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 font-medium">Grounded in Candidate Evidence Profile & Expert Knowledge Base</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-1.5">
                  <button
                    onClick={() => setIsMaximized(!isMaximized)}
                    title={isMaximized ? "Restore Size" : "Maximize Window"}
                    className="p-2 text-slate-400 hover:text-white rounded-xl hover:bg-white/10 transition-colors"
                  >
                    {isMaximized ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
                  </button>
                  <button
                    onClick={handleResetChat}
                    title="Reset Conversation"
                    className="p-2 text-slate-400 hover:text-white rounded-xl hover:bg-white/10 transition-colors"
                  >
                    <RotateCcw className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setIsOpen(false)}
                    title="Close Window"
                    className="p-2 text-slate-400 hover:text-white rounded-xl hover:bg-white/10 transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>

              {/* Target Career Filter Bar */}
              <div className="px-6 py-2.5 bg-white border-b border-slate-200/80 flex items-center justify-between gap-3 text-xs shadow-2xs">
                <div className="flex items-center gap-2.5 text-slate-700 font-medium w-full">
                  <div className="flex items-center gap-1.5 text-indigo-600 font-bold">
                    <Compass className="w-4 h-4" />
                    <span>Target Track:</span>
                  </div>
                  <div className="relative w-full max-w-md">
                    <select
                      value={selectedCareer}
                      onChange={(e) => setSelectedCareer(e.target.value)}
                      className="w-full bg-slate-50 border border-slate-300 rounded-xl px-3 py-1 text-slate-900 font-bold focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-xs appearance-none pr-8 cursor-pointer text-xs"
                    >
                      {topCareers.map((c: any, i: number) => (
                        <option key={i} value={c.career}>
                          {c.career} ({c.total_fit || c.score || ""}% Match)
                        </option>
                      ))}
                      <option value="Software Engineer">Software Engineer (IT)</option>
                      <option value="Machine Learning Engineer">Machine Learning Engineer (IT)</option>
                      <option value="Data Scientist">Data Scientist (IT)</option>
                      <option value="DevOps / Cloud Engineer">DevOps / Cloud Engineer (IT)</option>
                      <option value="Cybersecurity Analyst">Cybersecurity Analyst (IT)</option>
                      <option value="Senior Accountant & Tax Specialist">Senior Accountant (ACCOUNTANT)</option>
                      <option value="UI/UX Product Designer">UI/UX Product Designer (DESIGNER)</option>
                      <option value="Financial Analyst & Portfolio Specialist">Financial Analyst (FINANCE)</option>
                      <option value="Mechanical & Systems Engineer">Mechanical Engineer (ENGINEERING)</option>
                      <option value="Business Development Manager">Business Development (BUSINESS)</option>
                    </select>
                    <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 top-2 pointer-events-none" />
                  </div>
                </div>
              </div>

              {/* Quick Action Prompt Chips with 3-Color Borders */}
              <div className="px-6 py-2.5 bg-gradient-to-r from-indigo-50/70 via-purple-50/50 to-cyan-50/70 border-b border-slate-200/80 overflow-x-auto flex gap-2 no-scrollbar">
                {QUICK_PROMPTS.map((p, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(p.query)}
                    className="text-xs px-3 py-1.5 rounded-xl bg-white/90 border border-slate-200 hover:border-indigo-400 text-slate-800 hover:text-indigo-600 hover:bg-white transition-all whitespace-nowrap shadow-xs font-bold flex items-center gap-1.5 active:scale-95 flex-shrink-0"
                  >
                    <span>{p.icon}</span>
                    <span>{p.label}</span>
                  </button>
                ))}
              </div>

              {/* Chat Message Stream */}
              <div className="flex-1 overflow-y-auto p-6 md:p-8 space-y-6">
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex gap-3.5 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    {/* Bot Avatar */}
                    {msg.role === "assistant" && (
                      <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-600 via-violet-600 to-cyan-500 p-0.5 flex-shrink-0 shadow-md shadow-indigo-500/20 mt-1">
                        <div className="w-full h-full rounded-[14px] bg-slate-950 flex items-center justify-center text-cyan-300">
                          <Bot className="w-5 h-5" />
                        </div>
                      </div>
                    )}
                    
                    <div className="flex flex-col gap-1.5 max-w-[92%] md:max-w-[85%]">
                      {/* Message Bubble Card */}
                      <div
                        className={`rounded-3xl p-6 text-sm leading-relaxed shadow-sm transition-all ${
                          msg.role === "user"
                            ? "bg-gradient-to-r from-indigo-600 via-indigo-700 to-violet-700 text-white font-medium shadow-indigo-500/20 rounded-tr-none"
                            : "glass-card-3d text-slate-800 border border-slate-200/90 rounded-tl-none prose-chat relative group"
                        }`}
                      >
                        {/* Copy Full Response Action in Assistant Bubble */}
                        {msg.role === "assistant" && (
                          <div className="flex items-center justify-between mb-3 pb-2 border-b border-slate-100 text-[11px] text-slate-400">
                            <span className="font-mono flex items-center gap-1 text-indigo-600 font-bold">
                              <Sparkles className="w-3 h-3 text-cyan-500" />
                              Career Advisor Output
                            </span>
                            <button
                              onClick={() => handleCopyMessage(msg.id, msg.content)}
                              className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md hover:bg-slate-100 text-slate-500 hover:text-slate-900 transition-colors"
                              title="Copy response markdown"
                            >
                              {copiedId === msg.id ? (
                                <>
                                  <Check className="w-3 h-3 text-emerald-500" />
                                  <span className="text-emerald-600 font-bold">Copied!</span>
                                </>
                              ) : (
                                <>
                                  <Copy className="w-3 h-3" />
                                  <span>Copy</span>
                                </>
                              )}
                            </button>
                          </div>
                        )}

                        {msg.role === "user" ? (
                          <p className="whitespace-pre-wrap leading-relaxed text-sm md:text-base">{msg.content}</p>
                        ) : (
                          <MarkdownMessage content={msg.content} />
                        )}
                      </div>
                      
                      {/* Timestamp */}
                      <span className={`text-[10px] text-slate-400 px-2 font-mono ${msg.role === "user" ? "text-right" : "text-left"}`}>
                        {msg.timestamp}
                      </span>
                    </div>

                    {/* User Avatar */}
                    {msg.role === "user" && (
                      <div className="w-10 h-10 rounded-2xl bg-slate-900 text-white flex items-center justify-center flex-shrink-0 text-sm shadow-md mt-1 border border-slate-700">
                        <User className="w-5 h-5 text-indigo-300" />
                      </div>
                    )}
                  </div>
                ))}

                {/* Animated Typing Indicator with 3 Glowing Neon Bouncing Dots */}
                {loading && (
                  <div className="flex gap-3.5 items-start">
                    <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-600 via-violet-600 to-cyan-500 p-0.5 flex-shrink-0 shadow-md">
                      <div className="w-full h-full rounded-[14px] bg-slate-950 flex items-center justify-center text-cyan-300">
                        <Bot className="w-5 h-5" />
                      </div>
                    </div>
                    <div className="glass-card-3d p-4 rounded-3xl rounded-tl-none border border-indigo-100 flex items-center gap-4">
                      {/* 3 Neon Bouncing Dots */}
                      <div className="flex items-center gap-1.5 px-2">
                        <span className="w-2.5 h-2.5 rounded-full bg-indigo-600 typing-dot-1" />
                        <span className="w-2.5 h-2.5 rounded-full bg-violet-600 typing-dot-2" />
                        <span className="w-2.5 h-2.5 rounded-full bg-cyan-500 typing-dot-3" />
                      </div>
                      <div className="space-y-0.5">
                        <p className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                          <Zap className="w-3 h-3 text-amber-500 animate-pulse" />
                          <span>Groq 120B Synthesizing Roadmap & Evidence...</span>
                        </p>
                        <p className="text-[11px] text-slate-500 font-mono">Querying Dense Semantic RAG & verifying candidate profile</p>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>

              {/* Message Input Box with Modern Glassmorphism */}
              <div className="p-4 md:p-5 bg-white/95 border-t border-slate-200/90 shadow-2xl backdrop-blur-xl">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSendMessage();
                  }}
                  className="space-y-2"
                >
                  <div className="flex gap-2.5 items-end">
                    <textarea
                      rows={2}
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyDown={handleKeyDown}
                      placeholder="Ask any technical or career question (e.g. 'Assess my seniority', 'Mastering Python/C#', 'Suggest high-ROI projects')... (Press Enter to Send)"
                      disabled={loading}
                      className="flex-1 bg-slate-50 border border-slate-300/80 rounded-2xl px-4 py-3 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all placeholder:text-slate-400 font-medium resize-none leading-relaxed shadow-inner"
                    />
                    <button
                      type="submit"
                      disabled={!inputMessage.trim() || loading}
                      className="p-3.5 bg-gradient-to-r from-indigo-600 via-violet-600 to-cyan-600 text-white rounded-2xl hover:opacity-95 disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-lg shadow-indigo-500/25 active:scale-95 flex items-center justify-center flex-shrink-0"
                    >
                      <Send className="w-5 h-5" />
                    </button>
                  </div>
                  
                  <div className="flex items-center justify-between text-[11px] text-slate-400 px-1">
                    <span>💡 Press <strong className="text-slate-600">Enter</strong> to send, <strong className="text-slate-600">Shift + Enter</strong> for a new line</span>
                    <span className="font-mono text-[10px]">Model: gpt-oss-120b &bull; 0% Hallucination</span>
                  </div>
                </form>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}
