import { NextRequest, NextResponse } from 'next/server';
import { getAIProvider, getGenerativeProvider } from '@/lib/providers';

export async function POST(request: NextRequest) {
  try {
    const data = await request.json();
    const { candidateProfile } = data;

    if (!candidateProfile) {
      return NextResponse.json(
        { error: 'Missing candidateProfile' },
        { status: 400 }
      );
    }

    const aiProvider = getAIProvider();
    // generateCareerMap now maps to running career_engine.py
    const similarityData = await aiProvider.generateCareerMap(candidateProfile);
    
    // Add natural language explanation using Groq
    const groq = getGenerativeProvider();
    const explanation = await groq.explainCareerSimilarity(similarityData);

    return NextResponse.json({
        similarity_engine: similarityData,
        analysis: explanation
    });

  } catch (error: any) {
    console.error('API Error:', error);
    return NextResponse.json({ error: error.message || 'An unexpected error occurred' }, { status: 500 });
  }
}
