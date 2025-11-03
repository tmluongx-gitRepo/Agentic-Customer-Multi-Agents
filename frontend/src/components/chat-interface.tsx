/**
 * ChatInterface Component
 * BMAD Developer Implementation - Main container with state management and streaming
 */

'use client';

import { useState } from 'react';
import { Message } from '@/types';
import { MessageList } from '@/components/message-list';
import { MessageInput } from '@/components/message-input';
import { Card } from '@/components/ui/card';
import { streamChatMessage } from '@/lib/api';
import { AlertCircle } from 'lucide-react';

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSendMessage = async (content: string) => {
    // Add user message to the conversation
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Create a placeholder for the assistant's message
      const assistantMessageId = `assistant-${Date.now()}`;
      let assistantContent = '';

      // Add empty assistant message that will be updated as chunks arrive
      const assistantMessage: Message = {
        id: assistantMessageId,
        role: 'assistant',
        content: '',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Stream the response
      let routedTo: string | undefined;
      
      for await (const chunk of streamChatMessage(content)) {
        assistantContent += chunk;

        // Update the assistant message with accumulated content
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMessageId
              ? { ...msg, content: assistantContent }
              : msg
          )
        );
      }

      // Note: In the current implementation, routing info would need to be 
      // extracted from the response. For now, it's included in the message content.
      setIsLoading(false);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to send message. Please try again.');
      setIsLoading(false);

      // Remove the placeholder assistant message on error
      setMessages((prev) =>
        prev.filter((msg) => msg.role !== 'assistant' || msg.content !== '')
      );
    }
  };

  return (
    <Card className="flex flex-col h-[600px] w-full max-w-4xl mx-auto shadow-xl">
      {/* Header */}
      <div className="border-b p-4 bg-card">
        <h2 className="text-xl font-semibold">Advanced Customer Service AI</h2>
        <p className="text-sm text-muted-foreground">
          Multi-agent system: Billing Support • Technical Support • Policy & Compliance
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mx-4 mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-lg flex items-center gap-2">
          <AlertCircle className="h-4 w-4 text-destructive shrink-0" />
          <p className="text-sm text-destructive">{error}</p>
        </div>
      )}

      {/* Messages */}
      <MessageList messages={messages} isLoading={isLoading} />

      {/* Input */}
      <MessageInput
        onSendMessage={handleSendMessage}
        disabled={isLoading}
        placeholder={
          isLoading
            ? 'AI is thinking...'
            : 'Type your message...'
        }
      />
    </Card>
  );
}

