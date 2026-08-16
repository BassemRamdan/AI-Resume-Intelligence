// Calculates cosine similarity between two vectors
export function cosineSimilarity(vecA: number[], vecB: number[]): number {
  const dotProduct = vecA.reduce((sum, a, i) => sum + a * vecB[i], 0);
  const magnitudeA = Math.sqrt(vecA.reduce((sum, a) => sum + a * a, 0));
  const magnitudeB = Math.sqrt(vecB.reduce((sum, b) => sum + b * b, 0));
  if (magnitudeA === 0 || magnitudeB === 0) return 0;
  return dotProduct / (magnitudeA * magnitudeB);
}

export interface CandidateProfile {
  filename: string;
  predicted_category: string;
  skills: string[];
  education: string[];
  experience: string[];
  certifications: string[];
}

export interface JobRequirements {
  required_skills: string[];
  preferred_skills: string[];
  experience_requirements: string[];
  education_requirements: string[];
}

export interface JobData {
  job_id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  url: string;
  source: string;
  category: string;
  requirements: JobRequirements;
  embedding?: number[];
}

export interface EvidenceObject {
  skill: string;
  status: "FOUND" | "NOT_FOUND" | "UNKNOWN";
  source: string;
}

export function calculateMatchScore(
  candidate: CandidateProfile,
  resumeEmb: number[],
  job: JobData
): { score: number; matchedSkills: string[] } {
  // 1. Semantic Similarity (40%)
  const semanticScore = job.embedding ? Math.max(0, cosineSimilarity(resumeEmb, job.embedding)) : 0;

  // 2. Required Skill Coverage (40%)
  const reqSkills = new Set(job.requirements.required_skills.map((s) => s.toLowerCase()));
  const candSkills = new Set(candidate.skills.map((s) => s.toLowerCase()));
  
  const matched = [...reqSkills].filter((skill) => candSkills.has(skill));
  const skillScore = reqSkills.size > 0 ? matched.length / reqSkills.size : 1.0;

  // 3. Category Compatibility (20%)
  const catScore = candidate.predicted_category.toLowerCase() === job.category.toLowerCase() ? 1.0 : 0.0;

  // Final Weighted Score
  const finalScore = (semanticScore * 0.4) + (skillScore * 0.4) + (catScore * 0.2);

  return {
    score: Math.round(finalScore * 100 * 10) / 10, // Round to 1 decimal
    matchedSkills: matched,
  };
}

export function analyzeGaps(
  candidate: CandidateProfile,
  job: JobData,
  matchedSkills: string[]
): { missingSkills: string[]; evidence: EvidenceObject[] } {
  const reqSkills = new Set(job.requirements.required_skills.map((s) => s.toLowerCase()));
  const missing = [...reqSkills].filter((skill) => !matchedSkills.includes(skill));

  const evidence: EvidenceObject[] = [];
  
  matchedSkills.forEach((s) => {
    evidence.push({ skill: s, status: "FOUND", source: "Resume Entity Extraction" });
  });

  missing.forEach((s) => {
    evidence.push({ skill: s, status: "NOT_FOUND", source: "Job Description" });
  });

  return { missingSkills: missing, evidence };
}
