/**
 * MessageList Component
 * BMAD Developer Implementation - Display conversation history with auto-scroll
 */

'use client';

import { useEffect, useRef } from 'react';
import { Message } from '@/types';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { Bot, User } from 'lucide-react';

interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
}

export function MessageList({ messages, isLoading = false }: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center space-y-3">
          <div className="flex justify-center">
            <div className="rounded-full bg-primary/10 p-4">
              <Bot className="h-8 w-8 text-primary" />
            </div>
          </div>
          <div className="space-y-1">
            <h3 className="text-lg font-semibold">Welcome to Customer Service AI</h3>
            <p className="text-sm text-muted-foreground max-w-md">
              I'm here to help you with billing, technical support, and policy questions.
              Start a conversation by sending a message below.
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <ScrollArea className="flex-1 p-4">
      <div ref={scrollRef} className="space-y-4">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isLoading && (
          <div className="flex gap-3 items-start">
            <div className="rounded-full bg-primary/10 p-2 shrink-0">
              <Bot className="h-4 w-4 text-primary" />
            </div>
            <div className="rounded-2xl bg-muted px-4 py-2 max-w-[80%]">
              <div className="flex gap-1">
                <span className="animate-bounce">●</span>
                <span className="animate-bounce animation-delay-200">●</span>
                <span className="animate-bounce animation-delay-400">●</span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
    </ScrollArea>
  );
}

function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user';

  return (
    <div
      className={cn(
        'flex gap-3 items-start',
        isUser && 'flex-row-reverse'
      )}
    >
      <div
        className={cn(
          'rounded-full p-2 shrink-0',
          isUser ? 'bg-primary' : 'bg-primary/10'
        )}
      >
        {isUser ? (
          <User className={cn('h-4 w-4', 'text-primary-foreground')} />
        ) : (
          <Bot className="h-4 w-4 text-primary" />
        )}
      </div>
      <div
        className={cn(
          'rounded-2xl px-4 py-2 max-w-[80%] break-words',
          isUser
            ? 'bg-primary text-primary-foreground'
            : 'bg-muted text-foreground'
        )}
      >
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        <span className="text-xs opacity-70 mt-1 block">
          {new Date(message.timestamp).toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </span>
      </div>
    </div>
  );
}

