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
  ChevronDown
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import MarkdownMessage from "./MarkdownMessage";

interface CareerChatbotProps {
  candidateProfile: any;
  topCareers?: any[];
  defaultCareer?: string;
}

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

const QUICK_PROMPTS = [
  { 
    label: "🗺️ Detailed Career Roadmap", 
    query: "Generate a comprehensive, step-by-step milestone learning roadmap for my target career track based on my verified skills and missing competencies." 
  },
  { 
    label: "🔍 Skill Gap Diagnostics", 
    query: "Analyze my resume skills against the target career standards. What are my top high-priority skill gaps and how can I close them within 60-90 days?" 
  },
  { 
    label: "💻 Production Project Blueprints", 
    query: "Suggest 2-3 production-grade portfolio project blueprints with concrete architecture requirements that will prove my competency to hiring managers." 
  },
  { 
    label: "🏆 High-ROI Certifications", 
    query: "Which industry certifications offer the highest return on investment (ROI) for this career track, and which one should I prioritize?" 
  },
  { 
    label: "⚡ Senior Transition Strategy", 
    query: "What architectural, system design, and leadership competencies do I need to develop to successfully transition to a Senior role?" 
  }
];

export default function CareerChatbot({ candidateProfile, topCareers = [], defaultCareer }: CareerChatbotProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const [selectedCareer, setSelectedCareer] = useState<string>(
    defaultCareer || (topCareers.length > 0 ? topCareers[0].career : "Software Engineer")
  );

  const initialGreeting: ChatMessage = {
    role: "assistant",
    content: `### 👋 Welcome to CareerLens AI Principal Advisor!

I am your **AI Technical Career Architect & Senior Advisor**, powered by **120B Generative AI & Dense Semantic RAG Intelligence**.

Ask me anything about your career progression or deep technical topics:
- 🗺️ **Custom Roadmaps:** Step-by-step learning milestones tailored to your resume.
- 🔍 **Skill Gap Solutions:** Concrete actionable strategies to close missing competencies.
- 💻 **Production Project Blueprints:** End-to-end architectures to make your GitHub stand out.
- 💡 **Technical Deep-Dives:** Ask about any concept (e.g., *"How to learn Python/C#?"*, *"What is MLOps?"*, *"Design a Distributed Cache"*, *"Explain Microservices vs Monolith"*).`
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

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Floating Action Launcher Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <motion.button
          onClick={() => setIsOpen(true)}
          className="group flex items-center gap-3 px-6 py-4 bg-gradient-to-r from-indigo-600 via-indigo-700 to-violet-700 text-white rounded-full shadow-2xl hover:shadow-indigo-500/40 hover:scale-105 active:scale-95 transition-all font-extrabold border border-white/25 text-sm"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <div className="relative flex items-center justify-center">
            <Bot className="w-5 h-5 group-hover:rotate-12 transition-transform" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full animate-ping" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full" />
          </div>
          <span className="tracking-tight text-white font-bold">AI Career Advisor</span>
          <Sparkles className="w-4 h-4 text-amber-300 animate-pulse" />
        </motion.button>
      </div>

      {/* Large Slide-over Advisor Drawer / Modal */}
      <AnimatePresence>
        {isOpen && (
          <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/70 backdrop-blur-md transition-all">
            <motion.div
              initial={{ x: "100%", opacity: 0.8 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: "100%", opacity: 0.8 }}
              transition={{ type: "spring", damping: 28, stiffness: 240 }}
              className={`h-full bg-white shadow-2xl flex flex-col border-l border-slate-200 transition-all duration-300 ${
                isMaximized ? "w-full max-w-none" : "w-full md:w-[85vw] lg:w-[75vw] xl:max-w-5xl"
              }`}
            >
              {/* Header */}
              <div className="px-6 py-4 border-b border-slate-800 bg-gradient-to-r from-slate-950 via-slate-900 to-indigo-950 text-white flex items-center justify-between shadow-md">
                <div className="flex items-center gap-3.5">
                  <div className="w-11 h-11 rounded-2xl bg-indigo-600/30 border border-indigo-400/40 flex items-center justify-center text-indigo-300 shadow-inner">
                    <Bot className="w-6 h-6" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2.5">
                      <h3 className="font-black text-lg tracking-tight text-white">
                        CareerLens AI Principal Advisor
                      </h3>
                      <span className="text-[10px] uppercase font-black px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
                        120B Generative AI
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 font-medium">Deep Technical Counseling, System Architectures & Roadmaps</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setIsMaximized(!isMaximized)}
                    title={isMaximized ? "Restore Size" : "Maximize Window"}
                    className="p-2 text-slate-400 hover:text-white rounded-xl hover:bg-white/10 transition-colors"
                  >
                    {isMaximized ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
                  </button>
                  <button
                    onClick={handleResetChat}
                    title="Reset Conversation"
                    className="p-2 text-slate-400 hover:text-white rounded-xl hover:bg-white/10 transition-colors"
                  >
                    <RotateCcw className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => setIsOpen(false)}
                    title="Close"
                    className="p-2 text-slate-400 hover:text-white rounded-xl hover:bg-white/10 transition-colors"
                  >
                    <X className="w-6 h-6" />
                  </button>
                </div>
              </div>

              {/* Target Track Selector Bar */}
              <div className="px-6 py-3 bg-slate-50 border-b border-slate-200 flex items-center justify-between gap-3 text-xs">
                <div className="flex items-center gap-2.5 text-slate-600 font-medium w-full">
                  <Compass className="w-4 h-4 text-indigo-600 flex-shrink-0" />
                  <span className="flex-shrink-0 font-extrabold text-slate-800">Target Career Focus:</span>
                  <div className="relative w-full max-w-md">
                    <select
                      value={selectedCareer}
                      onChange={(e) => setSelectedCareer(e.target.value)}
                      className="w-full bg-white border border-slate-300 rounded-xl px-3.5 py-1.5 text-slate-900 font-bold focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm appearance-none pr-8 cursor-pointer text-xs"
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
                    <ChevronDown className="w-4 h-4 text-slate-400 absolute right-2.5 top-2.5 pointer-events-none" />
                  </div>
                </div>
              </div>

              {/* Quick Action Prompt Chips */}
              <div className="px-6 py-3 bg-indigo-50/40 border-b border-indigo-100/60 overflow-x-auto flex gap-2.5 no-scrollbar">
                {QUICK_PROMPTS.map((p, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(p.query)}
                    className="text-xs px-4 py-2 rounded-xl bg-white border border-indigo-200 text-indigo-700 hover:bg-indigo-600 hover:text-white transition-all whitespace-nowrap shadow-sm font-bold flex items-center gap-1.5 active:scale-95 flex-shrink-0"
                  >
                    {p.label}
                  </button>
                ))}
              </div>

              {/* Chat Message Stream with Rich Markdown */}
              <div className="flex-1 overflow-y-auto p-6 md:p-8 space-y-6 bg-slate-50/50">
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex gap-4 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    {msg.role === "assistant" && (
                      <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-indigo-600 via-indigo-700 to-violet-800 text-white flex items-center justify-center flex-shrink-0 text-sm shadow-md mt-1 border border-indigo-400/30">
                        <Bot className="w-5 h-5" />
                      </div>
                    )}
                    
                    <div
                      className={`max-w-[90%] md:max-w-[85%] rounded-3xl p-6 text-sm leading-relaxed shadow-sm ${
                        msg.role === "user"
                          ? "bg-indigo-600 text-white font-medium shadow-indigo-500/15 rounded-tr-none"
                          : "bg-white text-slate-800 border border-slate-200/90 shadow-slate-200/60 rounded-tl-none"
                      }`}
                    >
                      {msg.role === "user" ? (
                        <p className="whitespace-pre-wrap leading-relaxed text-sm md:text-base">{msg.content}</p>
                      ) : (
                        <MarkdownMessage content={msg.content} />
                      )}
                    </div>

                    {msg.role === "user" && (
                      <div className="w-10 h-10 rounded-2xl bg-slate-900 text-white flex items-center justify-center flex-shrink-0 text-sm shadow-md mt-1 border border-slate-700">
                        <User className="w-5 h-5" />
                      </div>
                    )}
                  </div>
                ))}

                {loading && (
                  <div className="flex gap-4 items-center p-5 bg-white rounded-3xl border border-slate-200 shadow-sm w-fit">
                    <div className="w-10 h-10 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
                      <RefreshCw className="w-5 h-5 animate-spin" />
                    </div>
                    <div className="space-y-1">
                      <p className="text-sm font-extrabold text-slate-800">120B AI Synthesizing Technical Reasoning...</p>
                      <p className="text-xs text-slate-500">Retrieving architectural standards, verified skills, and roadmap milestones.</p>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>

              {/* Spacious Message Input Box */}
              <div className="p-5 bg-white border-t border-slate-200 shadow-xl">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSendMessage();
                  }}
                  className="flex gap-3 items-end"
                >
                  <textarea
                    rows={2}
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask any technical or career question (e.g. 'How to learn Python/C#?', 'What is MLOps?', 'Project ideas')... (Press Enter to Send)"
                    disabled={loading}
                    className="flex-1 bg-slate-50 border border-slate-300 rounded-2xl px-5 py-3.5 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all placeholder:text-slate-400 font-medium resize-none leading-relaxed"
                  />
                  <button
                    type="submit"
                    disabled={!inputMessage.trim() || loading}
                    className="p-4 bg-indigo-600 text-white rounded-2xl hover:bg-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-indigo-500/30 active:scale-95 flex items-center justify-center flex-shrink-0"
                  >
                    <Send className="w-5 h-5" />
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
