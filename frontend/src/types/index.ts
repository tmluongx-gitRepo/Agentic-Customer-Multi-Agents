/**
 * Type definitions for the Customer Service AI Chat Interface
 * Integrated with FastAPI backend
 */

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  routed_to?: string; // Which agent handled the message
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  customer_id?: string;
}

export interface ChatResponse {
  response: string;
  routed_to: string; // Which agent handled the query (Billing, Technical, Policy)
  session_id: string;
  timestamp: string;
}

export interface StreamChunk {
  chunk: string;
  done: boolean;
}

export interface HealthResponse {
  status: string;
  version: string;
  timestamp: string;
}

