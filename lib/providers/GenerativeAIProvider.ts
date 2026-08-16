export interface GenerativeAIProvider {
  /**
   * Cleans, validates, and organizes the raw candidate profile extracted deterministically.
   */
  cleanProfile(rawProfile: any): Promise<any>;

  /**
   * Evaluates career readiness for adjacent/alternative roles (Career Map).
   */
  explainCareerSimilarity(similarityData: any): Promise<any>;
}
