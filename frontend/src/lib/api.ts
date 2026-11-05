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


const DEFAULT_API_BASE_URL = "";
const REQUEST_TIMEOUT_MS = 30_000;


function getApiBaseUrl(): string {

  const viteBaseUrl =
    typeof import.meta !== "undefined"
      ? import.meta.env?.VITE_API_BASE_URL
      : undefined;

  return (viteBaseUrl ?? DEFAULT_API_BASE_URL).replace(/\/$/, "");
}



export class ApiError extends Error {

  readonly status: number;



  constructor(message: string, status: number) {

    super(message);

    this.name = "ApiError";

    this.status = status;

  }

}


function isAgent(value: unknown): value is Agent {
  if (!value || typeof value !== "object") return false;
  const agent = value as Record<string, unknown>;
  return (
    typeof agent.id === "string" &&
    typeof agent.name === "string" &&
    typeof agent.icon === "string" &&
    typeof agent.tagline === "string"
  );
}

function isAgentList(value: unknown): value is Agent[] {
  return Array.isArray(value) && value.every(isAgent);
}

function isChatResponse(value: unknown): value is ChatResponse {
  if (!value || typeof value !== "object") return false;
  const response = value as Record<string, unknown>;
  return (
    isAgent(response.agent) &&
    typeof response.message === "string" &&
    response.message.length <= 4000 &&
    typeof response.elapsed_ms === "number" &&
    Number.isFinite(response.elapsed_ms) &&
    response.elapsed_ms >= 0
  );
}

function withTimeout(signal?: AbortSignal): {
  signal: AbortSignal;
  cleanup: () => void;
} {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(
    () => controller.abort("timeout"),
    REQUEST_TIMEOUT_MS,
  );
  const abortFromCaller = () => controller.abort(signal?.reason);

  if (signal?.aborted) {
    abortFromCaller();
  } else {
    signal?.addEventListener("abort", abortFromCaller, { once: true });
  }

  return {
    signal: controller.signal,
    cleanup: () => {
      window.clearTimeout(timeoutId);
      signal?.removeEventListener("abort", abortFromCaller);
    },
  };
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  const requestSignal = withTimeout(init?.signal ?? undefined);

  try {
    response = await fetch(`${getApiBaseUrl()}${path}`, {
      ...init,
      signal: requestSignal.signal,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        ...init?.headers,
      },
    });
  } catch (error) {
    if (init?.signal?.aborted) {
      throw error;
    }
    if (requestSignal.signal.aborted && requestSignal.signal.reason === "timeout") {
      throw new ApiError("The assistant took too long to respond. Please try again.", 408);
    }
    throw new ApiError("Could not reach the assistant API. Please try again.", 0);
  } finally {
    requestSignal.cleanup();
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



  const payload: unknown = await response.json();
  if (!payload) {
    throw new ApiError("The assistant returned an empty response.", 502);
  }
  return payload as T;
}


export function getAgents(signal?: AbortSignal): Promise<Agent[]> {
  return request<unknown>("/api/agents", { signal }).then((payload) => {
    if (!isAgentList(payload)) {
      throw new ApiError("The assistant returned an invalid agent list.", 502);
    }
    return payload;
  });
}


export function sendChat(

  requestBody: ChatRequest,

  signal?: AbortSignal,

): Promise<ChatResponse> {

  return request<unknown>("/api/chat", {
    method: "POST",

    body: JSON.stringify({

      agent_id: requestBody.agent_id,

      message: requestBody.message,

      history: requestBody.history ?? [],

      remember: requestBody.remember ?? true,

    }),

    signal,

  }).then((payload) => {
    if (!isChatResponse(payload)) {
      throw new ApiError("The assistant returned an invalid response.", 502);
    }
    return payload;
  });
}
