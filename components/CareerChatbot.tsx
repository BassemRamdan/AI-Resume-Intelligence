"use client";

import { useState, useRef, useEffect } from "react";
import { MessageSquare, Send, Bot, User, Sparkles, X, Compass, ChevronRight, CheckCircle2, Flame, RefreshCw, Layers } from "lucide-react";
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
  { label: "🗺️ Generate My Roadmap", query: "اعملي خطة طريق وخارطة تعلم متكاملة (Step-by-Step Roadmap) للمسار المستهدف بتاعي مع مشاريع مقترحة" },
  { label: "🔍 Analyze Missing Skills", query: "ايه المهارات والتقنيات الأساسية اللي ناقصاني عشان اكون مؤهل بقوة للتراك ده؟" },
  { label: "💻 Project Recommendations", query: "اقترح عليا أفكار مشاريع قوية ابنيها ف البورتفوليو تغطي المهارات اللي ناقصاني" },
  { label: "🎯 Transition Advice", query: "What are the key milestones to transition from junior to senior in this domain?" }
];

export default function CareerChatbot({ candidateProfile, topCareers = [], defaultCareer }: CareerChatbotProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedCareer, setSelectedCareer] = useState<string>(
    defaultCareer || (topCareers.length > 0 ? topCareers[0].career : "Software Engineer")
  );
  
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content: `👋 مرحباً بك! أنا **مستشارك المهني الذكي (AI Career Advisor)**.\n\nلقد قمت بتحليل سيرتك الذاتية ومهاراتك المسجلة. يمكنك سؤالي عن:\n- 🗺️ **خارطة طريق تعليمية (Learning Roadmap)** للوصول لأعلى مستوى في مسارك.\n- 🔍 **تحليل الفجوة المهارية (Skill Gaps)** وما تحتاجه للتميز.\n- 💻 **أفكار مشاريع عملية** لتقوية الـ Portfolio والـ GitHub.`
    }
  ]);
  
  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"chat" | "roadmap">("chat");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (defaultCareer) {
      setSelectedCareer(defaultCareer);
    } else if (topCareers.length > 0) {
      setSelectedCareer(topCareers[0].career);
    }
  }, [defaultCareer, topCareers]);

  useEffect(() => {
    if (isOpen && activeTab === "chat") {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isOpen, activeTab]);

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
          content: "⚠️ حدث خطأ في الاتصال بالمستشار الذكي. يرجى المحاولة مرة أخرى."
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
          className="flex items-center gap-3 px-5 py-3.5 bg-gradient-to-r from-indigo-600 to-violet-600 text-white rounded-full shadow-xl hover:shadow-indigo-500/25 hover:scale-105 active:scale-95 transition-all font-semibold"
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
          <div className="fixed inset-0 z-50 flex justify-end bg-slate-900/40 backdrop-blur-sm">
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className="w-full max-w-xl h-full bg-white shadow-2xl flex flex-col border-l border-slate-200"
            >
              {/* Header */}
              <div className="p-5 border-b border-slate-100 bg-gradient-to-r from-slate-900 to-indigo-950 text-white flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-indigo-500/20 border border-indigo-400/30 flex items-center justify-center text-indigo-300">
                    <Sparkles className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg leading-tight flex items-center gap-2">
                      CareerLens AI Advisor
                    </h3>
                    <p className="text-xs text-indigo-200">Grounded Career Counseling & Roadmaps</p>
                  </div>
                </div>
                
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-2 text-slate-400 hover:text-white rounded-lg hover:bg-white/10 transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Target Track Selector Bar */}
              <div className="px-5 py-3 bg-slate-50 border-b border-slate-200/80 flex items-center justify-between gap-2 text-xs">
                <div className="flex items-center gap-1.5 text-slate-600 font-medium truncate">
                  <Compass className="w-4 h-4 text-indigo-600 flex-shrink-0" />
                  <span>Target Career:</span>
                  <select
                    value={selectedCareer}
                    onChange={(e) => setSelectedCareer(e.target.value)}
                    className="bg-white border border-slate-200 rounded-lg px-2.5 py-1 text-slate-900 font-semibold focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  >
                    {topCareers.map((c: any, i: number) => (
                      <option key={i} value={c.career}>
                        {c.career} ({c.total_fit || c.score || ""}% Fit)
                      </option>
                    ))}
                    <option value="Software Engineer">Software Engineer</option>
                    <option value="Machine Learning Engineer">Machine Learning Engineer</option>
                    <option value="Data Scientist">Data Scientist</option>
                    <option value="DevOps / Cloud Engineer">DevOps / Cloud Engineer</option>
                    <option value="Senior Accountant & Tax Specialist">Senior Accountant</option>
                    <option value="UI/UX Product Designer">UI/UX Designer</option>
                    <option value="Business Development Manager">Business Development</option>
                  </select>
                </div>
              </div>

              {/* Quick Prompts Carousel */}
              <div className="px-4 py-2.5 bg-indigo-50/50 border-b border-indigo-100/60 overflow-x-auto flex gap-2 no-scrollbar">
                {QUICK_PROMPTS.map((p, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendMessage(p.query)}
                    className="text-xs px-3 py-1.5 rounded-full bg-white border border-indigo-200 text-indigo-700 hover:bg-indigo-600 hover:text-white transition-all whitespace-nowrap shadow-sm font-medium flex items-center gap-1"
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
                          : "bg-white text-slate-800 border border-slate-200 shadow-sm rounded-bl-none prose prose-sm prose-indigo"
                      }`}
                    >
                      <div className="whitespace-pre-wrap font-sans">
                        {msg.content}
                      </div>
                    </div>

                    {msg.role === "user" && (
                      <div className="w-8 h-8 rounded-full bg-slate-700 text-white flex items-center justify-center flex-shrink-0 text-xs shadow-sm mt-0.5">
                        <User className="w-4 h-4" />
                      </div>
                    )}
                  </div>
                ))}

                {loading && (
                  <div className="flex gap-3 items-center text-slate-400 text-sm">
                    <div className="w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center">
                      <RefreshCw className="w-4 h-4 animate-spin" />
                    </div>
                    <span className="italic">Career Advisor is formulating advice...</span>
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
                    placeholder="Ask about skill gaps, learning roadmap, or project ideas..."
                    disabled={loading}
                    className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all"
                  />
                  <button
                    type="submit"
                    disabled={!inputMessage.trim() || loading}
                    className="p-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow-sm"
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
