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
  MessageSquare,
  Zap,
  Target,
  Code2,
  Award,
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
    label: "🗺️ Career Roadmap", 
    query: "Generate a detailed, step-by-step milestone learning roadmap for my target career track based on my verified skills and missing competencies." 
  },
  { 
    label: "🔍 Skill Gap Analysis", 
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
    content: `### 👋 Welcome to CareerLens AI Advisor!

I am your **AI Technical Career Architect**, powered by **Dense Semantic RAG Intelligence**.

I can help you with:
- 🗺️ **Personalized Roadmaps:** Step-by-step milestones tailored to your verified skills.
- 🔍 **Skill Gap Solutions:** Concrete strategies to close high-priority technical gaps.
- 💻 **Production Project Blueprints:** Real-world architectural ideas for your GitHub portfolio.
- 💡 **Technical Concepts:** Ask me anything (e.g., *"What is Docker?"*, *"Explain Kafka vs RabbitMQ"*, *"How to design a Rate Limiter?"*).`
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

  return (
    <>
      {/* Floating Action Launcher Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <motion.button
          onClick={() => setIsOpen(true)}
          className="group flex items-center gap-3 px-5 py-3.5 bg-gradient-to-r from-indigo-600 via-indigo-700 to-violet-700 text-white rounded-full shadow-2xl hover:shadow-indigo-500/30 hover:scale-105 active:scale-95 transition-all font-bold border border-white/20"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <div className="relative flex items-center justify-center">
            <Bot className="w-5 h-5 group-hover:rotate-12 transition-transform" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full animate-ping" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-emerald-400 rounded-full" />
          </div>
          <span className="tracking-tight">AI Career Advisor</span>
          <Sparkles className="w-4 h-4 text-amber-300 animate-pulse" />
        </motion.button>
      </div>

      {/* Slide-over Advisor Drawer */}
      <AnimatePresence>
        {isOpen && (
          <div className="fixed inset-0 z-50 flex justify-end bg-slate-900/60 backdrop-blur-sm">
            <motion.div
              initial={{ x: "100%", opacity: 0.8 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: "100%", opacity: 0.8 }}
              transition={{ type: "spring", damping: 28, stiffness: 240 }}
              className="w-full max-w-2xl h-full bg-white shadow-2xl flex flex-col border-l border-slate-200"
            >
              {/* Header */}
              <div className="px-6 py-4.5 border-b border-slate-800 bg-gradient-to-r from-slate-950 via-slate-900 to-indigo-950 text-white flex items-center justify-between shadow-md">
                <div className="flex items-center gap-3.5">
                  <div className="w-10 h-10 rounded-xl bg-indigo-600/30 border border-indigo-400/40 flex items-center justify-center text-indigo-300 shadow-inner">
                    <Bot className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-extrabold text-base tracking-tight text-white">
                        CareerLens AI Advisor
                      </h3>
                      <span className="text-[10px] uppercase font-black px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
                        RAG Active
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 font-medium">Grounded Roadmaps & Deep Technical Guidance</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <button
                    onClick={handleResetChat}
                    title="Reset Conversation"
                    className="p-2 text-slate-400 hover:text-white rounded-xl hover:bg-white/10 transition-colors"
                  >
                    <RotateCcw className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setIsOpen(false)}
                    title="Close"
                    className="p-2 text-slate-400 hover:text-white rounded-xl hover:bg-white/10 transition-colors"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>

              {/* Target Track Selector Bar */}
              <div className="px-6 py-3 bg-slate-50 border-b border-slate-200 flex items-center justify-between gap-3 text-xs">
                <div className="flex items-center gap-2 text-slate-600 font-medium w-full">
                  <Compass className="w-4 h-4 text-indigo-600 flex-shrink-0" />
                  <span className="flex-shrink-0 font-bold text-slate-700">Target Track:</span>
                  <div className="relative w-full">
                    <select
                      value={selectedCareer}
                      onChange={(e) => setSelectedCareer(e.target.value)}
                      className="w-full bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-slate-900 font-bold focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm appearance-none pr-8 cursor-pointer"
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
              <div className="px-5 py-2.5 bg-indigo-50/40 border-b border-indigo-100/60 overflow-x-auto flex gap-2 no-scrollbar">
                {QUICK_PROMPTS.map((p, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(p.query)}
                    className="text-xs px-3.5 py-1.5 rounded-full bg-white border border-indigo-200 text-indigo-700 hover:bg-indigo-600 hover:text-white transition-all whitespace-nowrap shadow-sm font-semibold flex items-center gap-1.5 active:scale-95 flex-shrink-0"
                  >
                    {p.label}
                  </button>
                ))}
              </div>

              {/* Chat Message Stream with Rich Markdown */}
              <div className="flex-1 overflow-y-auto p-6 space-y-5 bg-slate-50/50">
                {messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`flex gap-3.5 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    {msg.role === "assistant" && (
                      <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-600 to-violet-700 text-white flex items-center justify-center flex-shrink-0 text-xs shadow-md mt-1 border border-indigo-400/20">
                        <Bot className="w-4 h-4" />
                      </div>
                    )}
                    
                    <div
                      className={`max-w-[88%] rounded-3xl p-5 text-sm leading-relaxed shadow-sm ${
                        msg.role === "user"
                          ? "bg-indigo-600 text-white font-medium shadow-indigo-500/10 rounded-tr-none"
                          : "bg-white text-slate-800 border border-slate-200/90 shadow-slate-200/50 rounded-tl-none"
                      }`}
                    >
                      {msg.role === "user" ? (
                        <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                      ) : (
                        <MarkdownMessage content={msg.content} />
                      )}
                    </div>

                    {msg.role === "user" && (
                      <div className="w-8 h-8 rounded-xl bg-slate-800 text-white flex items-center justify-center flex-shrink-0 text-xs shadow-md mt-1 border border-slate-700">
                        <User className="w-4 h-4" />
                      </div>
                    )}
                  </div>
                ))}

                {loading && (
                  <div className="flex gap-3.5 items-center p-4 bg-white rounded-2xl border border-slate-200/80 shadow-sm w-fit">
                    <div className="w-8 h-8 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
                      <RefreshCw className="w-4 h-4 animate-spin" />
                    </div>
                    <div className="space-y-1">
                      <p className="text-xs font-bold text-slate-800">Analyzing RAG Knowledge Base...</p>
                      <p className="text-[11px] text-slate-500">Synthesizing milestones, verified skills, and technical solutions.</p>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>

              {/* Message Input Box */}
              <div className="p-4.5 bg-white border-t border-slate-200 shadow-lg">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSendMessage();
                  }}
                  className="flex gap-2.5 items-center"
                >
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Ask anything (e.g. 'What is Docker?', 'Give me a roadmap', 'Project ideas')..."
                    disabled={loading}
                    className="flex-1 bg-slate-50 border border-slate-200 rounded-2xl px-4.5 py-3 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all placeholder:text-slate-400 font-medium"
                  />
                  <button
                    type="submit"
                    disabled={!inputMessage.trim() || loading}
                    className="p-3 bg-indigo-600 text-white rounded-2xl hover:bg-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-indigo-500/25 active:scale-95 flex items-center justify-center"
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
