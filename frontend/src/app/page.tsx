/**
 * Main Page - Customer Service AI Chat
 * BMAD Product Manager Vision: Clean, accessible, user-friendly interface
 */

import { ChatInterface } from '@/components/chat-interface';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-blue-950 to-indigo-950 p-4 md:p-8">
      <div className="container mx-auto max-w-6xl">
        {/* Hero Section */}
        <div className="text-center mb-8 space-y-2">
          <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-400">
            Customer Service AI
          </h1>
          <p className="text-slate-300 text-sm md:text-base max-w-2xl mx-auto">
            Experience intelligent customer support powered by specialized AI agents
            for billing, technical, and policy inquiries
          </p>
        </div>

        {/* Chat Interface */}
        <ChatInterface />

        {/* Footer Info */}
        <div className="mt-8 text-center text-xs text-slate-400">
          <p>
            Powered by LangGraph multi-agent architecture with OpenAI and AWS Bedrock
          </p>
        </div>
      </div>
    </main>
  );
}

