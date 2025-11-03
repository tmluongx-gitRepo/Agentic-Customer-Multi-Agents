# Customer Service AI - Frontend

A modern, responsive chat interface built with Next.js, React, and shadcn/ui for the Customer Service AI application. This frontend implements real-time streaming responses and session management for seamless conversational AI experiences.

## Features

✅ **Modern Chat UI**: Clean, user-friendly interface with shadcn/ui components  
✅ **Real-time Streaming**: AI responses stream for better UX  
✅ **Agent Routing Display**: Shows which specialist agent handled each query  
✅ **Conversation History**: Scrollable message list with auto-scroll  
✅ **Session Management**: Maintains conversation context using cookies  
✅ **Responsive Design**: Mobile-first design that works on all devices  
✅ **Dark Mode**: Beautiful dark theme  
✅ **Accessible**: Built with accessibility in mind using Radix UI primitives  
✅ **TypeScript**: Fully typed for better developer experience

## Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (Radix UI + Tailwind)
- **Icons**: Lucide React
- **HTTP Client**: Native Fetch API with ReadableStream

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx         # Root layout with metadata
│   │   ├── page.tsx           # Main chat page
│   │   └── globals.css        # Global styles and CSS variables
│   ├── components/
│   │   ├── ui/                # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   └── scroll-area.tsx
│   │   ├── chat-interface.tsx # Main chat container with state
│   │   ├── message-list.tsx   # Message display with auto-scroll
│   │   └── message-input.tsx  # Input field with keyboard support
│   ├── lib/
│   │   ├── api.ts            # API client with SSE streaming
│   │   └── utils.ts          # Utility functions (cn helper)
│   └── types/
│       └── index.ts          # TypeScript type definitions
├── public/                   # Static assets
├── components.json           # shadcn/ui configuration
├── tailwind.config.js        # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
├── next.config.js           # Next.js configuration
└── package.json             # Dependencies and scripts
```

## Getting Started

### Prerequisites

- **Node.js 18+** and npm (or yarn/pnpm)
- **Backend API running** on http://localhost:8000 (see [backend README](../backend/README.md))

### Installation

1. **Install dependencies:**

```bash
cd frontend
npm install
# or
yarn install
# or
pnpm install
```

2. **Configure environment variables:**

Create a `.env.local` file:

**Windows:**
```powershell
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

**Mac/Linux:**
```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

Or manually create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Run the development server:**

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

4. **Open your browser:**

Visit **http://localhost:3000** 🚀

You should see:
```
  ▲ Next.js 15.5.6
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000
✓ Starting...
✓ Ready in 21.9s
```

## Development

### Build for Production

```bash
npm run build
npm start
```

### Lint Code

```bash
npm run lint
```

## Usage

### Try These Example Queries

**Billing Support:**
- "What are your pricing plans?"
- "How much for 5 enterprise plans?"
- "What's your refund policy?"

**Technical Support:**
- "How do I reset my password?"
- "I'm getting an upload error, can you help?"
- "How do I configure two-factor authentication?"

**Policy & Compliance:**
- "What data do you collect?"
- "How long do you store my information?"
- "What is the cancellation process?"

### Features to Explore

1. **Agent Routing**: Watch how queries are routed to different specialists
   - Billing questions → Billing Support Agent (GPT-4o)
   - Technical questions → Technical Support Agent (GPT-4o)
   - Policy questions → Policy & Compliance Agent (GPT-4o-mini)

2. **Session Continuity**: Your conversation history is maintained across page refreshes

3. **Real-time Responses**: See AI responses stream in real-time

4. **Responsive UI**: Try it on mobile, tablet, and desktop

## Architecture Overview

### BMAD-METHOD Implementation

This frontend was developed following the **Breakthrough Method for Agile AI-Driven Development (BMAD)**, incorporating perspectives from multiple specialized roles:

#### Analyst Perspective
- Requirements gathering for real-time chat with streaming
- Session continuity for conversation context
- Seamless UX without exposing internal agent routing

#### Product Manager Perspective
- User stories focused on conversation flow
- Emphasis on modern, accessible, mobile-responsive design
- Clear value proposition for end users

#### Architect Perspective
- Component hierarchy with unidirectional data flow
- Server-Sent Events (SSE) for streaming implementation
- Cookie-based session management
- TypeScript for type safety

#### Developer Perspective
- Modular component structure
- Reusable shadcn/ui components
- Clean separation of concerns (UI, API, types)
- Comprehensive error handling

## Key Features Explained

### Streaming Implementation

The frontend uses an async generator function to handle streaming responses:

```typescript
// lib/api.ts
export async function* streamChatMessage(message: string) {
  const response = await fetch(`${API_URL}/chat`, { ... });
  const reader = response.body?.getReader();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    yield decoder.decode(value);
  }
}
```

Messages update in real-time as chunks arrive from the backend.

### Session Management

Sessions are managed via cookies using `js-cookie`:
- Backend returns `session_id` in response
- Frontend stores it automatically
- Subsequent requests include the session ID
- Enables conversation continuity

### Component Communication

- **Parent (ChatInterface)**: Manages conversation state
- **Children (MessageList, MessageInput)**: Receive props and callbacks
- Unidirectional data flow ensures predictable state updates

## API Integration

The frontend expects the following backend endpoints:

### POST /chat

**Request:**
```json
{
  "message": "string",
  "session_id": "string (optional)"
}
```

**Response (streaming or JSON):**
```json
{
  "response": "string",
  "agent_used": "string (optional)",
  "session_id": "string"
}
```

### GET /health

Health check endpoint for backend availability.

## Customization

### Changing API URL

Update `.env.local`:
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Modifying Theme

Edit `src/app/globals.css` to change color variables:
```css
:root {
  --primary: 222.2 47.4% 11.2%;
  /* ... other variables */
}
```

### Adding New Components

Use shadcn/ui CLI to add more components:
```bash
npx shadcn@latest add [component-name]
```

## Troubleshooting

### Backend Connection Issues

- Verify backend is running on configured URL
- Check CORS settings on backend allow frontend origin
- Inspect browser console for network errors

### Streaming Not Working

- Ensure backend sends proper streaming response
- Check `Content-Type` headers
- Fallback to non-streaming JSON mode if needed

### Session Not Persisting

- Verify cookies are enabled in browser
- Check backend returns `session_id` in response
- Inspect browser cookies for `chat_session_id`

## Contributing

This project follows the BMAD-METHOD development approach. When contributing:

1. Consider all personas (Analyst, PM, Architect, Developer)
2. Maintain type safety with TypeScript
3. Follow component structure conventions
4. Test responsive design on multiple screen sizes
5. Ensure accessibility standards are met

## License

This project is part of the Advanced Customer Service AI application.

---

Built with ❤️ using Next.js, React, and shadcn/ui

