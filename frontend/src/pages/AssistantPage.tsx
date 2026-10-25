"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Bot, Loader2, Menu, X } from "lucide-react";

import {
  ApiError,
  sendChat,
  type Agent,
  type ChatMessage,
} from "@/lib/api";
import { AppSidebar } from "@/components/navigation/app-sidebar";
import { Composer } from "@/components/chat/composer";
import {
  MessageList,
  type DisplayMessage,
} from "@/components/chat/message-list";
import { EmptyState } from "@/components/assistant/empty-state";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";

function createMessageId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

const MAX_DISPLAY_MESSAGES = 50;

export function AssistantPage() {
  const [activeAgent, setActiveAgent] = useState<Agent | null>(null);
  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [draft, setDraft] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [remember, setRemember] = useState(true);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const requestController = useRef<AbortController | null>(null);
  const isSubmitting = useRef(false);

  useEffect(() => {
    return () => requestController.current?.abort();
  }, []);

  const history = useMemo<ChatMessage[]>(
    () =>
      messages
        .filter((message) => !message.isError)
        .map(({ role, content, agent }) => ({ role, content, agent })),
    [messages],
  );

  const handleAgentsLoaded = useCallback((agents: Agent[]) => {
    setActiveAgent((current) => current ?? agents[0] ?? null);
  }, []);

  const handleSendMessage = useCallback(async () => {
    const message = draft.trim();
    const agent = activeAgent;

    if (!message || !agent || isProcessing || isSubmitting.current) return;
    isSubmitting.current = true;

    const priorHistory = history;
    const userMessage: DisplayMessage = {
      id: createMessageId(),
      role: "user",
      content: message,
    };

    setDraft("");
    setMessages((current) =>
      [...current, userMessage].slice(-MAX_DISPLAY_MESSAGES),
    );
    setIsProcessing(true);

    const controller = new AbortController();
    requestController.current = controller;
    const startedAt = performance.now();

    try {
      const response = await sendChat(
        {
          agent_id: agent.id,
          message,
          history: priorHistory,
          remember,
        },
        controller.signal,
      );

      const assistantMessage: DisplayMessage = {
        id: createMessageId(),
        role: "assistant",
        agent: response.agent.name,
        content: response.message,
        elapsedMs:
          response.elapsed_ms || Math.round(performance.now() - startedAt),
      };
      setMessages((current) =>
        [...current, assistantMessage].slice(-MAX_DISPLAY_MESSAGES),
      );
    } catch (reason: unknown) {
      if (reason instanceof DOMException && reason.name === "AbortError") {
        return;
      }

      const detail =
        reason instanceof ApiError
          ? reason.message
          : "The assistant could not complete that request. Please try again.";

      const errorMessage: DisplayMessage = {
        id: createMessageId(),
        role: "assistant",
        agent: agent.name,
        content: detail,
        elapsedMs: Math.round(performance.now() - startedAt),
        isError: true,
      };
      setMessages((current) =>
        [...current, errorMessage].slice(-MAX_DISPLAY_MESSAGES),
      );
    } finally {
      isSubmitting.current = false;
      if (requestController.current === controller) {
        requestController.current = null;
        setIsProcessing(false);
      }
    }
  }, [activeAgent, draft, history, isProcessing, remember]);

  const handleAgentChange = useCallback(
    (agent: Agent) => {
      if (isProcessing || agent.id === activeAgent?.id) return;
      setMessages([]);
      setDraft("");
      setActiveAgent(agent);
    },
    [activeAgent?.id, isProcessing],
  );

  const handleNewChat = useCallback(() => {
    if (isProcessing) return;
    setMessages([]);
    setDraft("");
  }, [isProcessing]);

  const handlePromptSelect = useCallback((prompt: string) => {
    setDraft(prompt);
  }, []);

  const handleMobileAgentChange = useCallback((agent: Agent) => {
    handleAgentChange(agent);
    setIsMobileSidebarOpen(false);
  }, [handleAgentChange]);

  const handleMobileNewChat = useCallback(() => {
    handleNewChat();
    setIsMobileSidebarOpen(false);
  }, [handleNewChat]);

  return (
    <div className="flex h-dvh overflow-hidden bg-background">
      <div className="hidden shrink-0 md:block">
        <AppSidebar
          activeAgentId={activeAgent?.id ?? ""}
          hasMessages={messages.length > 0}
          isProcessing={isProcessing}
          onAgentChange={handleAgentChange}
          onAgentsLoaded={handleAgentsLoaded}
          onNewChat={handleNewChat}
          onRememberChange={setRemember}
          remember={remember}
        />
      </div>

      {isMobileSidebarOpen && (
        <div className="fixed inset-0 z-40 md:hidden">
          <button
            aria-label="Close navigation"
            className="absolute inset-0 bg-slate-950/40"
            onClick={() => setIsMobileSidebarOpen(false)}
            type="button"
          />
          <div className="relative h-full w-[min(18rem,85vw)] shadow-xl">
            <AppSidebar
              activeAgentId={activeAgent?.id ?? ""}
              hasMessages={messages.length > 0}
              isProcessing={isProcessing}
              onAgentChange={handleMobileAgentChange}
              onAgentsLoaded={handleAgentsLoaded}
              onNewChat={handleMobileNewChat}
              onRememberChange={setRemember}
              remember={remember}
            />
            <button
              aria-label="Close navigation"
              className="absolute right-3 top-4 inline-flex size-9 items-center justify-center rounded-lg border bg-card text-muted-foreground shadow-sm"
              onClick={() => setIsMobileSidebarOpen(false)}
              type="button"
            >
              <X className="size-4" aria-hidden="true" />
            </button>
          </div>
        </div>
      )}

      <main className="flex min-w-0 flex-1 flex-col">
        <header className="flex min-h-16 items-center gap-3 border-b px-3 py-4 sm:px-6">
          <button
            aria-label="Open navigation"
            className="inline-flex size-9 shrink-0 items-center justify-center rounded-lg border text-muted-foreground md:hidden"
            onClick={() => setIsMobileSidebarOpen(true)}
            type="button"
          >
            <Menu className="size-4" aria-hidden="true" />
          </button>
          <Avatar className="size-9 rounded-xl">
            <AvatarFallback className="rounded-xl bg-primary/10 text-base">
              {activeAgent ? activeAgent.icon : <Bot className="size-4" />}
            </AvatarFallback>
          </Avatar>
          <div className="min-w-0">
            <h1 className="truncate text-sm font-semibold">
              {activeAgent?.name ?? "Assistant Hub"}
            </h1>
            <p className="truncate text-xs text-muted-foreground">
              {activeAgent?.tagline ?? "Loading your specialist workspace…"}
            </p>
          </div>
        </header>

        <div className="min-h-0 flex-1 overflow-y-auto">
          {!activeAgent ? (
            <div className="flex h-full items-center justify-center gap-2 text-sm text-muted-foreground">
              <Loader2 className="size-4 animate-spin" aria-hidden="true" />
              Loading specialists…
            </div>
          ) : messages.length === 0 ? (
            <EmptyState
              agent={activeAgent}
              onPromptSelect={handlePromptSelect}
            />
          ) : (
            <MessageList
              activeAgent={activeAgent}
              isProcessing={isProcessing}
              messages={messages}
            />
          )}
        </div>

        <Composer
          disabled={!activeAgent || isProcessing}
          onChange={setDraft}
          onSubmit={handleSendMessage}
          placeholder={
            activeAgent
              ? `Message ${activeAgent.name}…`
              : "Loading assistant…"
          }
          value={draft}
        />
      </main>
    </div>
  );
}

export default AssistantPage;
