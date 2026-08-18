"use client";

import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { CheckCircle2, Circle, Copy, Check, Terminal, Sparkles } from "lucide-react";

interface MarkdownMessageProps {
  content: string;
}

export default function MarkdownMessage({ content }: MarkdownMessageProps) {
  return (
    <div className="markdown-content text-slate-200 space-y-3 leading-relaxed">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ node, ...props }) => (
            <h1 className="text-xl font-black text-white mt-4 mb-2 pb-1 border-b border-slate-700 flex items-center gap-2" {...props} />
          ),
          h2: ({ node, ...props }) => (
            <h2 className="text-lg font-bold text-white mt-3 mb-2 flex items-center gap-2" {...props} />
          ),
          h3: ({ node, ...props }) => (
            <h3 className="text-base font-extrabold text-cyan-300 mt-3 mb-1.5 flex items-center gap-2 bg-slate-900/90 p-2.5 rounded-xl border border-cyan-800/50 shadow-sm" {...props} />
          ),
          h4: ({ node, ...props }) => (
            <h4 className="text-sm font-bold text-indigo-300 mt-3 mb-1 flex items-center gap-1.5" {...props} />
          ),
          p: ({ node, ...props }) => (
            <p className="text-sm text-slate-300 leading-relaxed mb-2" {...props} />
          ),
          ul: ({ node, ...props }) => (
            <ul className="space-y-1.5 my-2 pl-2" {...props} />
          ),
          ol: ({ node, ...props }) => (
            <ol className="list-decimal pl-5 space-y-1.5 my-2 text-sm text-slate-300 font-medium" {...props} />
          ),
          li: ({ node, children, ...props }) => {
            return (
              <li className="text-sm text-slate-300 flex items-start gap-2 leading-normal list-none" {...props}>
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 mt-2 flex-shrink-0 shadow-xs shadow-cyan-400" />
                <span className="flex-1">{children}</span>
              </li>
            );
          },
          table: ({ node, ...props }) => (
            <div className="overflow-x-auto my-4 rounded-xl border border-slate-800 shadow-md bg-slate-950/80">
              <table className="w-full text-left text-xs md:text-sm border-collapse" {...props} />
            </div>
          ),
          thead: ({ node, ...props }) => (
            <thead className="bg-slate-900 text-white border-b border-slate-800 font-bold uppercase text-[11px] tracking-wider" {...props} />
          ),
          tbody: ({ node, ...props }) => (
            <tbody className="divide-y divide-slate-800/80 bg-slate-950/40" {...props} />
          ),
          tr: ({ node, ...props }) => (
            <tr className="hover:bg-slate-900/60 transition-colors" {...props} />
          ),
          th: ({ node, ...props }) => (
            <th className="py-3 px-4 font-extrabold text-cyan-300" {...props} />
          ),
          td: ({ node, ...props }) => (
            <td className="py-2.5 px-4 text-slate-300 leading-relaxed align-top" {...props} />
          ),
          hr: ({ node, ...props }) => (
            <hr className="border-t border-slate-800 my-4" {...props} />
          ),
          strong: ({ node, ...props }) => (
            <strong className="font-bold text-white bg-slate-800/90 px-1 py-0.5 rounded text-xs tracking-tight" {...props} />
          ),
          blockquote: ({ node, ...props }) => (
            <blockquote className="border-l-4 border-cyan-500 pl-4 py-1.5 my-3 bg-cyan-950/30 rounded-r-xl italic text-sm text-cyan-200 border-t border-b border-r border-cyan-900/30" {...props} />
          ),
          code: ({ node, className, children, ...props }: any) => {
            const isInline = !className;
            if (isInline) {
              return (
                <code className="bg-slate-900 text-cyan-300 px-1.5 py-0.5 rounded-md font-mono text-xs font-semibold border border-slate-800" {...props}>
                  {children}
                </code>
              );
            }
            return <CodeBlock code={String(children).replace(/\n$/, "")} />;
          },
          input: ({ node, ...props }: any) => {
            if (props.type === "checkbox") {
              const checked = props.checked;
              return checked ? (
                <CheckCircle2 className="w-4 h-4 text-emerald-400 inline-block mr-1.5 flex-shrink-0" />
              ) : (
                <Circle className="w-4 h-4 text-slate-500 inline-block mr-1.5 flex-shrink-0" />
              );
            }
            return <input {...props} />;
          }
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

function CodeBlock({ code }: { code: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="my-3 rounded-xl overflow-hidden border border-slate-800 bg-slate-950 text-slate-100 font-mono text-xs shadow-xl">
      <div className="flex items-center justify-between px-3.5 py-2 bg-slate-900 border-b border-slate-800 text-slate-400">
        <span className="flex items-center gap-1.5 text-[11px] font-semibold text-cyan-400">
          <Terminal className="w-3.5 h-3.5" /> Code Snippet
        </span>
        <button
          onClick={handleCopy}
          className="flex items-center gap-1 text-[11px] px-2 py-0.5 rounded hover:bg-slate-800 text-slate-300 hover:text-white transition-colors"
        >
          {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
          <span>{copied ? "Copied" : "Copy"}</span>
        </button>
      </div>
      <div className="p-3.5 overflow-x-auto">
        <pre>{code}</pre>
      </div>
    </div>
  );
}
