export interface ResumeAnalysisProvider {
  /**
   * Extract a candidate profile from a PDF resume buffer.
   */
  extractProfile(fileBuffer: Buffer, filename: string): Promise<any>;



  /**
   * Generate a deterministic career map (Top matching roles)
   */
  generateCareerMap(candidateProfile: any): Promise<any>;
}
