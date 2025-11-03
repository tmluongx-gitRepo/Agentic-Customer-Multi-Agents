# Frontend Setup Guide

This guide will walk you through setting up the Customer Service AI frontend application.

## Quick Start

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

This will install all required dependencies including:
- Next.js 15
- React 18
- TypeScript
- Tailwind CSS
- shadcn/ui components
- Lucide React icons
- js-cookie for session management

### Step 2: Configure Environment

Create a `.env.local` file in the frontend directory:

```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

Or manually create `.env.local` with:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Note:** Change the URL if your backend is running on a different port or host.

### Step 3: Run Development Server

```bash
npm run dev
```

The application will start at [http://localhost:3000](http://localhost:3000)

## Verifying the Setup

1. Open your browser to `http://localhost:3000`
2. You should see the chat interface with a welcome message
3. If the backend is not running, you'll see connection errors when sending messages

## Backend Requirements

The frontend expects a FastAPI backend with the following endpoint:

### POST /chat
- **Request Body**: `{ "message": "string", "session_id": "string (optional)" }`
- **Response**: `{ "response": "string", "session_id": "string", "agent_used": "string (optional)" }`

### GET /health
- **Response**: `{ "status": "healthy" }`

## Production Build

To create an optimized production build:

```bash
npm run build
npm start
```

The production server will run on port 3000 by default.

## Common Issues

### Port 3000 Already in Use

Run on a different port:
```bash
PORT=3001 npm run dev
```

### Module Not Found Errors

Make sure all dependencies are installed:
```bash
rm -rf node_modules package-lock.json
npm install
```

### Backend Connection Errors

1. Verify backend is running: `curl http://localhost:8000/health`
2. Check CORS settings on backend
3. Verify `NEXT_PUBLIC_API_URL` in `.env.local`

### TypeScript Errors

Run type checking:
```bash
npx tsc --noEmit
```

## Development Tips

### Hot Reload

Next.js automatically reloads when you save files. Changes to:
- Components (`.tsx` files)
- Styles (`.css` files)
- Configuration (requires restart)

### Adding shadcn/ui Components

To add more UI components:

```bash
npx shadcn@latest add [component-name]
```

Example:
```bash
npx shadcn@latest add dialog
npx shadcn@latest add toast
```

### Component Structure

```
src/
├── app/          # Next.js app router pages
├── components/   # React components
│   └── ui/      # shadcn/ui components
├── lib/         # Utility functions
└── types/       # TypeScript types
```

## Testing the Chat Interface

1. Start the backend (see backend README)
2. Start the frontend: `npm run dev`
3. Open browser to `http://localhost:3000`
4. Type a message and press Enter or click Send
5. Watch the AI response stream in real-time

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |

**Important:** Variables starting with `NEXT_PUBLIC_` are exposed to the browser.

## Project Commands

```bash
npm run dev      # Start development server
npm run build    # Create production build
npm run start    # Start production server
npm run lint     # Run ESLint
```

## Next Steps

1. Customize the theme in `src/app/globals.css`
2. Add additional features to components
3. Integrate with your backend API
4. Deploy to production (Vercel, Netlify, etc.)

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [shadcn/ui Components](https://ui.shadcn.com)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

For issues or questions, refer to the main README.md or project documentation.

