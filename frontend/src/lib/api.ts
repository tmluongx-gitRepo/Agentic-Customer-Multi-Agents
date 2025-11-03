/**
 * API Client for Advanced Customer Service AI
 * Integrates with FastAPI backend multi-agent system
 * Handles session management and streaming responses
 */

import { ChatRequest, ChatResponse, HealthResponse } from '@/types';
import Cookies from 'js-cookie';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const SESSION_COOKIE_NAME = 'chat_session_id';

/**
 * Get current session ID from cookies
 */
export function getSessionId(): string | undefined {
  return Cookies.get(SESSION_COOKIE_NAME);
}

/**
 * Store session ID in cookies
 */
export function setSessionId(sessionId: string): void {
  Cookies.set(SESSION_COOKIE_NAME, sessionId, { expires: 7 }); // 7 days
}

/**
 * Clear session ID from cookies
 */
export function clearSession(): void {
  Cookies.remove(SESSION_COOKIE_NAME);
}

/**
 * Send message to backend with simulated streaming response
 * The FastAPI backend returns a complete response, which we stream character-by-character
 * for a better UX
 */
export async function* streamChatMessage(
  message: string
): AsyncGenerator<string, void, unknown> {
  const sessionId = getSessionId();
  
  const request: ChatRequest = {
    message,
    session_id: sessionId,
  };

  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorText}`);
    }

    const data: ChatResponse = await response.json();
    
    // Store session ID from backend
    if (data.session_id) {
      setSessionId(data.session_id);
    }
    
    // Simulate streaming by yielding character by character for better UX
    const responseText = data.response;
    const routingInfo = `\n\n_Handled by: ${data.routed_to}_`;
    const fullText = responseText + routingInfo;
    
    for (const char of fullText) {
      yield char;
      await new Promise(resolve => setTimeout(resolve, 15)); // 15ms delay per character
    }
    
  } catch (error) {
    console.error('Error streaming chat message:', error);
    throw error;
  }
}

/**
 * Send message without streaming (direct response)
 */
export async function sendChatMessage(message: string): Promise<ChatResponse> {
  const sessionId = getSessionId();
  
  const request: ChatRequest = {
    message,
    session_id: sessionId,
  };

  try {
    const response = await fetch(`${API_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorText}`);
    }

    const data: ChatResponse = await response.json();
    
    // Store session ID
    if (data.session_id) {
      setSessionId(data.session_id);
    }

    return data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
}

/**
 * Health check endpoint
 */
export async function healthCheck(): Promise<HealthResponse | null> {
  try {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) {
      return null;
    }
    return await response.json();
  } catch (error) {
    console.error('Health check failed:', error);
    return null;
  }
}

/**
 * Get session count from backend (for monitoring)
 */
export async function getSessionCount(): Promise<number | null> {
  try {
    const response = await fetch(`${API_URL}/sessions/count`);
    if (!response.ok) {
      return null;
    }
    const data = await response.json();
    return data.active_sessions;
  } catch (error) {
    console.error('Error fetching session count:', error);
    return null;
  }
}

