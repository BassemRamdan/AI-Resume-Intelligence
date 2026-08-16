"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";

interface CandidateContextType {
  profile: any;
  setProfile: (profile: any) => void;
  clearProfile: () => void;
  isHydrated: boolean;
}

const CandidateContext = createContext<CandidateContextType | undefined>(undefined);

export function CandidateProvider({ children }: { children: React.ReactNode }) {
  const [profile, setProfileState] = useState<any>(null);
  const [isHydrated, setIsHydrated] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  // Hydrate from localStorage on mount
  useEffect(() => {
    const savedProfile = localStorage.getItem("careerlens_profile");
    if (savedProfile) {
      try {
        setProfileState(JSON.parse(savedProfile));
      } catch (err) {
        console.error("Failed to parse profile", err);
      }
    }
    setIsHydrated(true);
  }, []);

  // Sync to localStorage
  const setProfile = (newProfile: any) => {
    if (newProfile) {
      try {
        // Prevent QuotaExceededError by stripping massive raw text snippets
        const profileToSave = { ...newProfile };
        if (profileToSave.raw_text_snippet) {
          delete profileToSave.raw_text_snippet;
        }
        localStorage.setItem("careerlens_profile", JSON.stringify(profileToSave));
      } catch (err) {
        console.error("Failed to save profile to localStorage. It may exceed quota.", err);
      }
    } else {
      localStorage.removeItem("careerlens_profile");
    }
    setProfileState(newProfile);
  };

  const clearProfile = () => {
    setProfile(null);
  };

  // Route protection
  useEffect(() => {
    if (isHydrated) {
      const protectedRoutes = ["/profile", "/careers", "/jobs", "/analyze"];
      if (protectedRoutes.includes(pathname) && !profile) {
        router.push("/upload");
      }
    }
  }, [isHydrated, profile, pathname, router]);

  return (
    <CandidateContext.Provider value={{ profile, setProfile, clearProfile, isHydrated }}>
      {children}
    </CandidateContext.Provider>
  );
}

export function useCandidate() {
  const context = useContext(CandidateContext);
  if (context === undefined) {
    throw new Error("useCandidate must be used within a CandidateProvider");
  }
  return context;
}
