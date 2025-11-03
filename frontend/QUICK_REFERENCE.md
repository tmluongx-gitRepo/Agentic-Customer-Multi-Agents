# Quick Reference Card

## 🚀 Getting Started (30 seconds)

```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
npm run dev
# Open http://localhost:3000
```

---

## 📂 Key Files

| File | Purpose |
|------|---------|
| `src/components/chat-interface.tsx` | Main chat container with state |
| `src/components/message-list.tsx` | Display messages with auto-scroll |
| `src/components/message-input.tsx` | User input field |
| `src/lib/api.ts` | API client with streaming |
| `src/types/index.ts` | TypeScript types |
| `src/app/page.tsx` | Main page |

---

## 🔧 Commands

```bash
npm run dev      # Development server
npm run build    # Production build
npm run lint     # Lint code
```

---

## 🌐 Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🎨 Customization Quick Tips

### Change Theme Colors
Edit `src/app/globals.css`:
```css
:root {
  --primary: 222.2 47.4% 11.2%;  /* Change this */
}
```

### Add New shadcn Component
```bash
npx shadcn@latest add [component-name]
```

### Modify API URL
Change `.env.local`:
```
NEXT_PUBLIC_API_URL=https://your-api.com
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 3000 in use | `PORT=3001 npm run dev` |
| Backend connection fails | Check CORS, verify backend running |
| Module not found | `rm -rf node_modules && npm install` |
| TypeScript errors | `npx tsc --noEmit` |

---

## 📊 Component Props

### ChatInterface
No props (standalone component)

### MessageList
- `messages: Message[]` - Array of messages
- `isLoading?: boolean` - Show loading indicator

### MessageInput
- `onSendMessage: (message: string) => void` - Callback
- `disabled?: boolean` - Disable input
- `placeholder?: string` - Placeholder text

---

## 🔗 API Integration

```typescript
// Expected backend response
{
  "response": "string",
  "session_id": "string",
  "agent_used": "string (optional)"
}
```

---

## 📱 Responsive Breakpoints

- Mobile: `< 768px`
- Tablet: `768px - 1024px`
- Desktop: `> 1024px`

---

## ✅ Checklist Before Deployment

- [ ] Update `NEXT_PUBLIC_API_URL` for production
- [ ] Run `npm run build` successfully
- [ ] Test on mobile devices
- [ ] Verify backend CORS configuration
- [ ] Check environment variables
- [ ] Test streaming functionality
- [ ] Verify session persistence

---

## 📚 Documentation

- `README.md` - Complete documentation
- `SETUP.md` - Setup instructions
- `IMPLEMENTATION.md` - Implementation details
- `PROJECT_SUMMARY.md` - Full summary

---

## 🎯 Key Features

✅ Real-time streaming  
✅ Session management  
✅ Responsive design  
✅ Error handling  
✅ Keyboard shortcuts  
✅ Auto-scroll  
✅ Loading states  
✅ Accessibility  

---

**Need Help?** Check `SETUP.md` for detailed troubleshooting

