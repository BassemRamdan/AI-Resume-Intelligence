import Groq from "groq-sdk";
import { GenerativeAIProvider } from "./GenerativeAIProvider";

export class GroqProvider implements GenerativeAIProvider {
  private client: Groq;
  private model: string;

  constructor() {
    // Requires GROQ_API_KEY to be set in environment
    this.client = new Groq({ apiKey: process.env.GROQ_API_KEY || '' });
    this.model = 'allam-2-7b';
  }

  async cleanProfile(rawProfile: any): Promise<any> {
    const prompt = `
You are CareerLens AI, an expert AI pipeline validator.
Your job is to clean, validate, and organize the raw candidate profile extracted deterministically.
STRICT RULE: You may ONLY return information supported by the supplied 'evidence' or 'raw_text_snippet'.
If evidence is missing, output 'UNKNOWN' for strings, or 'NOT_FOUND' for evidence fields. NEVER guess or fabricate information.

RAW PROFILE:
${JSON.stringify(rawProfile, null, 2)}

Return a strict JSON object following this exact schema:
{
  "identity": { "name": "", "email": "", "phone": "", "location": "" },
  "summary": "Professional summary paragraph if found, else UNKNOWN",
  "skills": [ { "name": "", "normalized_name": "", "category": "Programming|ML/AI|Data|Web|Cloud|Tools|Soft Skills", "evidence": "", "confidence": 0.0 } ],
  "education": [ { "institution": "", "degree": "", "field": "", "start_date": "", "end_date": "", "evidence": "", "confidence": 0.0 } ],
  "experience": [ { "job_title": "", "company": "", "location": "", "start_date": "", "end_date": "", "responsibilities": [], "technologies": [], "evidence": "", "confidence": 0.0 } ],
  "projects": [ { "name": "", "description": "", "technologies": [], "role": "", "links": [], "evidence": "", "confidence": 0.0 } ],
  "certifications": [ { "name": "", "issuer": "", "date": "", "evidence": "", "confidence": 0.0 } ],
  "languages": [],
  "achievements": [],
  "career_signal": { "dataset_category": "", "confidence": 0.0 }
}
`;
    return this.callGroq(prompt);
  }

  async explainCareerSimilarity(similarityData: any): Promise<any> {
    const prompt = `
You are CareerLens AI, an expert career analyst.
The machine learning pipeline has evaluated the candidate's career fit using a deterministic engine with strict percentages.
Your job is to provide a grounded explanation for WHY the candidate matches the Top Career Fits based ONLY on the evidence provided in the JSON.

RAW ENGINE DATA:
${JSON.stringify(similarityData, null, 2)}

STRICT RULES:
1. DO NOT invent skills, projects, or experience. Use ONLY what is provided in the JSON.
2. The score is deterministic. Explain the score using the evidence (Skill Match, Project Match, etc.).

Return a strict JSON object with this schema:
{
  "classification_analysis": "1 sentence explaining the primary classification.",
  "top_careers": [
    {
      "career": "The exact career name (e.g. Machine Learning Engineer)",
      "total_fit": "The total_fit percentage",
      "why": "A 2-3 sentence explanation connecting their matched skills and projects to this career.",
      "missing_evidence": "A 1 sentence explanation of what they are missing (e.g. Docker, MLOps) based on the missing_skills array."
    }
  ],
  "similar_profiles_analysis": "A 1-2 sentence summary explaining the KNN semantic similarity peer group."
}
`;
    try {
      return await this.callGroq(prompt);
    } catch (e) {
      console.warn("Groq failed, falling back to deterministic explanation generation:", e);
      // Fallback deterministic response so the UI NEVER breaks
      const primaryCat = similarityData?.classification?.category || "General";
      const fitList = similarityData?.career_fit || [];
      return {
        classification_analysis: `Primary classification signal indicates highest compatibility with ${primaryCat}.`,
        top_careers: fitList.slice(0, 3).map((m: any) => ({
          career: m.career,
          total_fit: m.total_fit,
          why: `Calculated ${m.total_fit}% deterministic fit based on verified skills (${m.evidence?.matched_skills?.join(', ') || 'strong foundational skills'}), experience match, and domain similarity.`,
          missing_evidence: m.evidence?.missing_skills?.length > 0 
            ? `Recommended development in: ${m.evidence.missing_skills.slice(0, 3).join(', ')}.`
            : "Strong direct alignment with core requirements."
        })),
        similar_profiles_analysis: "Semantic similarity peer group calculated via KNN embeddings comparison against benchmark profiles."
      };
    }
  }

  private async callGroq(prompt: string): Promise<any> {
    if (!process.env.GROQ_API_KEY) {
      throw new Error("GROQ_API_KEY is not configured.");
    }
    
    const candidateModels = ['allam-2-7b', 'qwen/qwen3.6-27b'];
    
    for (const model of candidateModels) {
      try {
        const chatCompletion = await this.client.chat.completions.create({
          messages: [{ role: "user", content: prompt }],
          model: model,
          response_format: { type: "json_object" },
          temperature: 0.2,
        });

        const content = chatCompletion.choices[0]?.message?.content;
        if (content) {
          return JSON.parse(content);
        }
      } catch (error: any) {
        console.error(`Groq error with model ${model}:`, error?.message || error);
      }
    }
    throw new Error("Failed to generate AI reasoning with available models.");
  }
}
