import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import { CandidateProvider } from "@/lib/store/CandidateStore";
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
  title: "CareerLens AI - Premium Career Intelligence",
  description: "Understand where you are. Discover where you fit. Know what to learn next.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-slate-50 text-slate-900 font-sans">
        <CandidateProvider>
          <header className="sticky top-0 z-50 w-full border-b border-slate-200 bg-white/80 backdrop-blur">
            <div className="container mx-auto flex h-16 items-center justify-between px-4">
              <Link href="/" className="flex items-center gap-2">
                <div className="h-8 w-8 rounded-lg bg-indigo-600 flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </div>
                <span className="text-xl font-bold tracking-tight">CareerLens AI</span>
              </Link>
              <nav className="hidden md:flex gap-6 text-sm font-medium text-slate-600">
                <Link href="/upload" className="hover:text-indigo-600 transition-colors">Analyze Resume</Link>
                <Link href="/profile" className="hover:text-indigo-600 transition-colors">Profile</Link>
                <Link href="/careers" className="hover:text-indigo-600 transition-colors">Career Map</Link>
              </nav>
              <Link href="/upload" className="rounded-full bg-slate-900 px-5 py-2 text-sm font-semibold text-white hover:bg-slate-800 transition-colors">
                Get Started
              </Link>
            </div>
          </header>
          <main className="flex-1">
            {children}
          </main>
        </CandidateProvider>
      </body>
    </html>
  );
}
