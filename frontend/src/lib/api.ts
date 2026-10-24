export type ChatRole = "user" | "assistant";

export interface Agent {
  id: string;
  name: string;
  icon: string;
  tagline: string;
}

export interface ChatMessage {
  role: ChatRole;
  content: string;
  agent?: string;
}

export interface ChatRequest {
  agent_id: string;
  message: string;
  history?: ChatMessage[];
  remember?: boolean;
}

export interface ChatResponse {
  agent: Agent;
  message: string;
  elapsed_ms: number;
}

export interface ApiErrorPayload {
  detail?: string;
}

const DEFAULT_API_BASE_URL = "http://localhost:8001";

function getApiBaseUrl(): string {
  const viteBaseUrl =
    typeof import.meta !== "undefined"
      ? import.meta.env?.VITE_API_BASE_URL
      : undefined;

  return (viteBaseUrl || DEFAULT_API_BASE_URL).replace(/\/$/, "");
}

export class ApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${getApiBaseUrl()}${path}`, {
      ...init,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        ...init?.headers,
      },
    });
  } catch (error) {
    const message =
      error instanceof Error ? error.message : "The API request failed";
    throw new ApiError(`Could not reach the assistant API: ${message}`, 0);
  }

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;

    try {
      const payload = (await response.json()) as ApiErrorPayload;
      if (payload.detail) {
        detail = payload.detail;
      }
    } catch {
      // Preserve the HTTP status when the server did not return JSON.
    }

    throw new ApiError(detail, response.status);
  }

  return (await response.json()) as T;
}

export function getAgents(signal?: AbortSignal): Promise<Agent[]> {
  return request<Agent[]>("/api/agents", { signal });
}

export function sendChat(
  requestBody: ChatRequest,
  signal?: AbortSignal,
): Promise<ChatResponse> {
  return request<ChatResponse>("/api/chat", {
    method: "POST",
    body: JSON.stringify({
      agent_id: requestBody.agent_id,
      message: requestBody.message,
      history: requestBody.history ?? [],
      remember: requestBody.remember ?? true,
    }),
    signal,
  });
}
