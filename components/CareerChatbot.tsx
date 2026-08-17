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
  CheckCircle2, 
  Layers, 
  Flame, 
  BookOpen, 
  Code2 
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface CareerChatbotProps {
  candidateProfile: any;
  topCareers?: any[];
  defaultCareer?: string;
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

const QUICK_PROMPTS = [
  { 
    label: "🗺️ Personalized Roadmap", 
    query: "Generate a detailed, step-by-step milestone learning roadmap for my target career track based on my verified skills and missing competencies." 
  },
  { 
    label: "🔍 Missing Skills & Gaps", 
    query: "Analyze my resume skills against the target career standards. What are my top high-priority skill gaps and how can I close them?" 
  },
  { 
    label: "💻 Project Blueprints", 
    query: "Suggest 2-3 production-grade portfolio project blueprints with concrete architecture requirements that will prove my competency to hiring managers." 
  },
  { 
    label: "🏆 High-ROI Certifications", 
    query: "Which industry certifications offer the highest return on investment (ROI) for this career track, and which one should I prioritize?" 
  },
  { 
    label: "⚡ Senior Level Transition", 
    query: "What architectural and leadership competencies do I need to develop to successfully transition from junior/mid to a senior engineering role?" 
  }
];

export default function CareerChatbot({ candidateProfile, topCareers = [], defaultCareer }: CareerChatbotProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedCareer, setSelectedCareer] = useState<string>(
    defaultCareer || (topCareers.length > 0 ? topCareers[0].career : "Software Engineer")
  );

  const initialGreeting: ChatMessage = {
    role: "assistant",
    content: `👋 Welcome! I am your **CareerLens AI Advisor** equipped with **RAG Knowledge Base Intelligence**.\n\nI have analyzed your verified resume profile against industry standards. How can I help accelerate your growth?\n\n- 🗺️ **Personalized Roadmap:** Step-by-step learning milestones from foundations to production mastery.\n- 🔍 **Skill Gap Analysis:** Targeted evaluation of missing high-value competencies.\n- 💻 **Project Blueprints:** Production-ready project ideas to build an impactful portfolio.`
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
  }, [messages, isOpen]);

  const handleResetChat = () => {
    setMessages([initialGreeting]);
  };

  const handleSendMessage = async (textToSend?: string) => {
    const query = (textToSend || inputMessage).trim();
    if (!query || loading) return;

    const userMsg: ChatMessage = { role: "user", content: query };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setInputMessage("");
    setLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: updatedMessages,
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
        { role: "assistant", content: data.response || "No response received." }
      ]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠️ An error occurred while communicating with the AI Advisor. Please try again."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Floating Action Launcher Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <motion.button
          onClick={() => setIsOpen(true)}
          className="flex items-center gap-3 px-5 py-3.5 bg-gradient-to-r from-indigo-600 to-violet-600 text-white rounded-full shadow-2xl hover:shadow-indigo-500/30 hover:scale-105 active:scale-95 transition-all font-semibold border border-white/10"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <div className="relative">
            <Bot className="w-5 h-5" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full animate-ping" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full" />
          </div>
          <span>AI Career Advisor</span>
        </motion.button>
      </div>

      {/* Slide-over Advisor Drawer */}
      <AnimatePresence>
        {isOpen && (
          <div className="fixed inset-0 z-50 flex justify-end bg-slate-900/50 backdrop-blur-sm">
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", damping: 26, stiffness: 220 }}
              className="w-full max-w-2xl h-full bg-white shadow-2xl flex flex-col border-l border-slate-200"
            >
              {/* Header */}
              <div className="p-5 border-b border-slate-100 bg-gradient-to-r from-slate-950 via-slate-900 to-indigo-950 text-white flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-indigo-500/20 border border-indigo-400/30 flex items-center justify-center text-indigo-300 shadow-inner">
                    <Sparkles className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg leading-tight flex items-center gap-2">
                      CareerLens AI Advisor
                      <span className="text-[10px] uppercase font-extrabold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-400/30">
                        RAG-Enhanced
                      </span>
                    </h3>
                    <p className="text-xs text-slate-400">Grounded Career Roadmaps & Technical Guidance</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <button
                    onClick={handleResetChat}
                    title="Reset Conversation"
                    className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-white/10 transition-colors"
                  >
                    <RotateCcw className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setIsOpen(false)}
                    title="Close"
                    className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-white/10 transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>

              {/* Target Track Selector Bar */}
              <div className="px-5 py-3 bg-slate-50 border-b border-slate-200/80 flex items-center justify-between gap-3 text-xs">
                <div className="flex items-center gap-2 text-slate-600 font-medium w-full">
                  <Compass className="w-4 h-4 text-indigo-600 flex-shrink-0" />
                  <span className="flex-shrink-0">Target Track:</span>
                  <select
                    value={selectedCareer}
                    onChange={(e) => setSelectedCareer(e.target.value)}
                    className="bg-white border border-slate-200 rounded-lg px-3 py-1 text-slate-900 font-semibold focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full shadow-sm"
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
                    <option value="Business Development Manager">Business Development Manager (BUSINESS-DEVELOPMENT)</option>
                  </select>
                </div>
              </div>

              {/* Quick Action Prompt Chips */}
              <div className="px-4 py-2.5 bg-indigo-50/50 border-b border-indigo-100/60 overflow-x-auto flex gap-2 no-scrollbar">
                {QUICK_PROMPTS.map((p, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(p.query)}
                    className="text-xs px-3.5 py-1.5 rounded-full bg-white border border-indigo-200 text-indigo-700 hover:bg-indigo-600 hover:text-white transition-all whitespace-nowrap shadow-sm font-medium flex items-center gap-1.5 active:scale-95"
                  >
                    {p.label}
                  </button>
                ))}
              </div>

              {/* Chat Message Stream */}
              <div className="flex-1 overflow-y-auto p-5 space-y-4 bg-slate-50/40">
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    {msg.role === "assistant" && (
                      <div className="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center flex-shrink-0 text-xs shadow-sm mt-0.5">
                        <Bot className="w-4 h-4" />
                      </div>
                    )}
                    
                    <div
                      className={`max-w-[85%] rounded-2xl p-4 text-sm leading-relaxed ${
                        msg.role === "user"
                          ? "bg-indigo-600 text-white shadow-md rounded-br-none"
                          : "bg-white text-slate-800 border border-slate-200 shadow-sm rounded-bl-none prose prose-sm prose-slate max-w-none"
                      }`}
                    >
                      <div className="whitespace-pre-wrap font-sans text-sm leading-relaxed">
                        {msg.content}
                      </div>
                    </div>

                    {msg.role === "user" && (
                      <div className="w-8 h-8 rounded-full bg-slate-800 text-white flex items-center justify-center flex-shrink-0 text-xs shadow-sm mt-0.5">
                        <User className="w-4 h-4" />
                      </div>
                    )}
                  </div>
                ))}

                {loading && (
                  <div className="flex gap-3 items-center text-slate-400 text-sm p-3 bg-white rounded-2xl border border-slate-200 w-fit">
                    <div className="w-6 h-6 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center">
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    </div>
                    <span className="italic text-xs text-slate-500 font-medium">
                      Retrieving RAG roadmap knowledge & formulating advice...
                    </span>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>

              {/* Message Input Box */}
              <div className="p-4 bg-white border-t border-slate-200">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSendMessage();
                  }}
                  className="flex gap-2"
                >
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Ask about skill gaps, learning roadmap milestones, or project blueprints..."
                    disabled={loading}
                    className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all placeholder:text-slate-400"
                  />
                  <button
                    type="submit"
                    disabled={!inputMessage.trim() || loading}
                    className="p-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md active:scale-95 flex items-center justify-center"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </form>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}
