import { ResumeAnalysisProvider } from "./ResumeAnalysisProvider";

export class RemoteResumeProvider implements ResumeAnalysisProvider {
  private url: string;
  private token: string;

  constructor(url: string, token: string) {
    this.url = url;
    this.token = token;
  }

  private async fetchAPI(endpoint: string, method: string, body?: any): Promise<any> {
    const response = await fetch(`${this.url}${endpoint}`, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`,
      },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (!response.ok) {
      let errorText = response.statusText;
      try {
        const errorData = await response.json();
        errorText = errorData.error || errorData.detail || errorText;
      } catch (e) {}
      throw new Error(`Remote API Error: ${errorText}`);
    }

    return await response.json();
  }

  async extractProfile(fileBuffer: Buffer, filename: string): Promise<any> {
    // For file uploads, we need multipart/form-data
    const formData = new FormData();
    const blob = new Blob([new Uint8Array(fileBuffer)], { type: 'application/pdf' });
    formData.append('file', blob, filename);

    const response = await fetch(`${this.url}/api/extract`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
      },
      body: formData,
    });

    if (!response.ok) {
      let errorText = response.statusText;
      try {
        const errorData = await response.json();
        errorText = errorData.error || errorData.detail || errorText;
      } catch (e) {}
      throw new Error(`Remote API Error: ${errorText}`);
    }

    const rawProfile = await response.json();
    
    // Clean with Groq just like LocalResumeProvider
    const { GroqProvider } = require("./GroqProvider");
    const groq = new GroqProvider();
    const cleanedProfile = await groq.cleanProfile(rawProfile);
    
    // Inject deterministic fields back
    if (rawProfile.career_signal) {
      cleanedProfile.career_signal = rawProfile.career_signal;
    }
    cleanedProfile.filename = filename;
    cleanedProfile.raw_text_snippet = rawProfile.raw_text_snippet;
    
    return cleanedProfile;
  }



  async generateCareerMap(candidateProfile: any): Promise<any> {
    return await this.fetchAPI('/api/career-map', 'POST', {
      candidateProfile
    });
  }
}
