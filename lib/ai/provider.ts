import { HfInference } from "@huggingface/inference";

// Create AIProvider abstraction
export class AIProvider {
  private hf: HfInference;
  private embedModel: string;
  private genModel: string;

  constructor() {
    // In production, pass HF_TOKEN from environment
    this.hf = new HfInference(process.env.HF_TOKEN);
    this.embedModel = process.env.EMBEDDING_MODEL || "sentence-transformers/all-MiniLM-L6-v2";
    this.genModel = process.env.GENERATION_MODEL || "google/flan-t5-small";
  }

  async encode(texts: string[]): Promise<number[][]> {
    try {
      // The featureExtraction method returns embeddings
      const res = await this.hf.featureExtraction({
        model: this.embedModel,
        inputs: texts,
      });
      return res as number[][];
    } catch (error) {
      console.error("Error during embedding generation:", error);
      // Fallback dummy embeddings for offline/demo if API fails
      return texts.map(() => Array(384).fill(0.1));
    }
  }

  async generate(prompt: string): Promise<string> {
    try {
      const res = await this.hf.textGeneration({
        model: this.genModel,
        inputs: prompt,
        parameters: { max_new_tokens: 50 },
      });
      return res.generated_text;
    } catch (error) {
      console.error("Error during text generation:", error);
      return "Recommendation currently unavailable due to API limits.";
    }
  }
}

export const aiProvider = new AIProvider();
