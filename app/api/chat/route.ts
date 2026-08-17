import { NextRequest, NextResponse } from 'next/server';

export const maxDuration = 60;

export async function POST(request: NextRequest) {
  try {
    const data = await request.json();
    const { messages, candidateProfile, targetCareer } = data;

    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return NextResponse.json(
        { error: 'Messages array is required' },
        { status: 400 }
      );
    }

    const aiServiceUrl = process.env.AI_SERVICE_URL || 'http://127.0.0.1:8000';

    const response = await fetch(`${aiServiceUrl}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages,
        candidateProfile: candidateProfile || {},
        targetCareer: targetCareer || null
      }),
    });

    if (!response.ok) {
      throw new Error(`FastAPI chat failed with status ${response.status}`);
    }

    const result = await response.json();
    return NextResponse.json(result);

  } catch (error: any) {
    console.error('Chat API Error:', error);
    const msg = error.message || 'An unexpected error occurred';
    
    // Fallback response if FastAPI is not reachable
    const fallbackResponse = `### 🎯 Career Guidance & Roadmap Assistant
    
I am ready to help you level up your career! You can ask me:
- **"What skills do I need to learn next?"**
- **"Give me a step-by-step roadmap for my target role"**
- **"What projects should I build to enhance my portfolio?"**
- **"كيف يمكنني تطوير مهاراتي في هذا المسار؟"**`;

    return NextResponse.json({ response: fallbackResponse });
  }
}
