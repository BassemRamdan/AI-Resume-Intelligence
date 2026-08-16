import { NextRequest, NextResponse } from 'next/server';
import { getAIProvider } from '@/lib/providers';

export const maxDuration = 60;
export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('resume') as File | null;
    
    if (!file) {
      return NextResponse.json(
        { error: 'No resume file provided' },
        { status: 400 }
      );
    }
    
    if (file.type !== 'application/pdf') {
      return NextResponse.json(
        { error: 'Only PDF files are supported for MVP' },
        { status: 400 }
      );
    }

    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    // Use AI Provider to extract profile securely (local or remote)
    const aiProvider = getAIProvider();
    const profile = await aiProvider.extractProfile(buffer, file.name);

    return NextResponse.json(profile);

  } catch (error: any) {
    console.error('API Error:', error);
    const msg = error.message || 'An unexpected error occurred';
    
    if (msg.includes('fetch') || msg.includes('ECONNREFUSED')) {
      return NextResponse.json({ error: 'AI service unavailable or starting up. Please ensure FastAPI is running.' }, { status: 503 });
    }
    
    return NextResponse.json({ error: msg }, { status: 500 });
  }
}
