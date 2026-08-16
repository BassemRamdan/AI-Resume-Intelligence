export * from './ResumeAnalysisProvider';
export * from './LocalResumeProvider';
export * from './RemoteResumeProvider';
export * from './GenerativeAIProvider';
export * from './GroqProvider';

import { ResumeAnalysisProvider } from "./ResumeAnalysisProvider";
import { LocalResumeProvider } from "./LocalResumeProvider";
import { RemoteResumeProvider } from "./RemoteResumeProvider";
import { GenerativeAIProvider } from "./GenerativeAIProvider";
import { GroqProvider } from "./GroqProvider";

export function getAIProvider(): ResumeAnalysisProvider {
  const url = process.env.AI_SERVICE_URL;
  const token = process.env.AI_SERVICE_TOKEN || "";
  
  if (url) {
    return new RemoteResumeProvider(url, token);
  }
  
  return new LocalResumeProvider();
}

export function getGenerativeProvider(): GenerativeAIProvider {
  return new GroqProvider();
}
