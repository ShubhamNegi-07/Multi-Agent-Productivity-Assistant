"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Activity,
  ArrowLeft,
  Bot,
  ChevronDown,
  CircleDot,
  CirclePlus,
  Loader2,
  Menu,
  RotateCw,
} from "lucide-react";

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
import { AgentIcon } from "@/components/assistant/agent-icon";
import { Sheet, SheetContent } from "@/components/ui/sheet";

function createMessageId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

const MAX_DISPLAY_MESSAGES = 50;

interface AssistantPageProps {
  onBackToLanding?: () => void;
}

export function AssistantPage({ onBackToLanding }: AssistantPageProps) {
  const [activeAgent, setActiveAgent] = useState<Agent | null>(null);
  const [messages, setMessages] = useState<DisplayMessage[]>([]);
  const [draft, setDraft] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const remember = true;
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const [agentLoadError, setAgentLoadError] = useState<string | null>(null);
  const requestController = useRef<AbortController | null>(null);
  const isSubmitting = useRef(false);
  const chatScrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    return () => requestController.current?.abort();
  }, []);

  useEffect(() => {
    const scrollContainer = chatScrollRef.current;
    if (!scrollContainer) return;

    const frame = window.requestAnimationFrame(() => {
      scrollContainer.scrollTo({
        top: scrollContainer.scrollHeight,
        behavior: "smooth",
      });
    });

    return () => window.cancelAnimationFrame(frame);
  }, [messages.length, isProcessing]);

  const history = useMemo<ChatMessage[]>(
    () =>
      messages
        .filter((message) => !message.isError)
        .map(({ role, content, agent }) => ({ role, content, agent })),
    [messages],
  );

  const handleAgentsLoaded = useCallback((agents: Agent[]) => {
    setAgentLoadError(null);
    setActiveAgent((current) => current ?? agents[0] ?? null);
  }, []);

  const handleAgentsError = useCallback((message: string) => {
    setAgentLoadError(message);
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
    <div className="app-bg relative flex h-dvh overflow-hidden bg-[#151313] text-[#F4F4F4]">
      {/* Desktop Sidebar */}
      <div className="hidden shrink-0 md:block">
        <AppSidebar
          activeAgentId={activeAgent?.id ?? ""}
          isProcessing={isProcessing}
          onAgentChange={handleAgentChange}
          onAgentsLoaded={handleAgentsLoaded}
          onAgentsError={handleAgentsError}
          onNewChat={handleNewChat}
          onBackToLanding={onBackToLanding}
        />
      </div>

      {/* Mobile Drawer */}
      <Sheet open={isMobileSidebarOpen} onOpenChange={setIsMobileSidebarOpen}>
        <SheetContent>
          <AppSidebar
            activeAgentId={activeAgent?.id ?? ""}
            isProcessing={isProcessing}
            onAgentChange={handleMobileAgentChange}
            onAgentsLoaded={handleAgentsLoaded}
            onAgentsError={handleAgentsError}
            onNewChat={handleMobileNewChat}
            onBackToLanding={onBackToLanding}
          />
        </SheetContent>
      </Sheet>

      <main className="relative flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden">
        {/* App Bar Header */}
        <header className="flex h-16 items-center gap-3.5 border-b border-[#312E2E] bg-[#151313]/90 px-4 backdrop-blur-xl sm:px-6">
          <button
            aria-label="Open navigation"
            className="inline-flex size-9 shrink-0 items-center justify-center rounded-lg text-[#817F7F] hover:bg-[#201D1D] hover:text-[#F4F4F4] md:hidden"
            onClick={() => setIsMobileSidebarOpen(true)}
            type="button"
          >
            <Menu className="size-4" aria-hidden="true" />
          </button>

          {onBackToLanding && (
            <button
              className="flex items-center gap-1.5 rounded-full border border-[#312E2E] bg-[#201D1D] px-3 py-1 text-xs text-[#817F7F] transition-colors hover:text-[#A1FF62] md:hidden"
              onClick={onBackToLanding}
              type="button"
            >
              <ArrowLeft className="size-3" />
              <span>Landing</span>
            </button>
          )}

          <Avatar className="size-8 rounded-lg">
            <AvatarFallback className="rounded-lg bg-[#201D1D] border border-[#312E2E] text-[#A1FF62]">
              {activeAgent ? <AgentIcon agent={activeAgent} className="size-4" /> : <Bot className="size-4" />}
            </AvatarFallback>
          </Avatar>

          <div className="min-w-0 border-l border-[#312E2E] pl-3.5">
            <div className="flex items-center gap-2 text-base sm:text-lg">
              <span className="text-[#817F7F]">OmniDesk</span>
              <span className="text-[#817F7F]/40">/</span>
              <span className="font-hafferVf font-bold text-[#F4F4F4]">{activeAgent?.name ?? "Workspace"}</span>
              <ChevronDown className="size-4 text-[#817F7F]" />
            </div>
          </div>

          <div className="ml-auto flex items-center gap-3">
            <button
              className="hidden items-center gap-1.5 rounded-full border border-[#312E2E] bg-[#201D1D] px-3.5 py-1.5 text-xs font-medium text-[#F4F4F4] transition-all hover:border-[#A1FF62]/40 hover:text-[#A1FF62] sm:inline-flex"
              disabled={isProcessing}
              onClick={handleNewChat}
              type="button"
            >
              <CirclePlus className="size-3 text-[#A1FF62]" />
              New thread
            </button>
            <div className="hidden items-center gap-1.5 rounded-full border border-[#312E2E] bg-[#201D1D] px-3.5 py-1.5 text-xs text-[#817F7F] sm:flex">
              <Activity className="size-3 text-[#6840FF]" />
              Focus Mode
            </div>
            <div className="flex items-center gap-1.5 rounded-full border border-[#312E2E] bg-[#201D1D] px-3.5 py-1.5 text-xs text-[#817F7F]">
              <CircleDot className="size-3 fill-[#A1FF62] text-[#A1FF62] animate-pulse" />
              <span className="hidden sm:inline text-[#F4F4F4]">Engine Ready</span>
            </div>
          </div>
        </header>

        {/* Chat Scroll View */}
        <div
          className="scrollbar-hidden min-h-0 flex-1 overflow-y-auto pb-56 pt-4"
          ref={chatScrollRef}
        >
          {!activeAgent ? (
            <div className="mx-auto flex h-full max-w-md flex-col items-center justify-center px-6 text-center">
              {agentLoadError ? (
                <>
                  <div className="flex size-12 items-center justify-center rounded-2xl border border-red-500/30 bg-red-500/10 text-red-400">
                    <RotateCw className="size-5" />
                  </div>
                  <h2 className="mt-5 font-hafferVf text-lg font-bold text-[#F4F4F4]">Workspace Unavailable</h2>
                  <p className="mt-2 text-xs leading-6 text-[#817F7F]">
                    {agentLoadError} Ensure backend is running on port 8001.
                  </p>
                </>
              ) : (
                <>
                  <Loader2 className="size-5 animate-spin text-[#A1FF62]" />
                  <p className="mt-3 text-xs text-[#817F7F]">Loading agent desks…</p>
                </>
              )}
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

        {/* Floating Composer */}
        <Composer
          agent={activeAgent}
          disabled={!activeAgent || isProcessing}
          onChange={setDraft}
          onSubmit={handleSendMessage}
          placeholder={
            activeAgent
              ? `Ask ${activeAgent.name}…`
              : "Loading assistant…"
          }
          value={draft}
        />
      </main>
    </div>
  );
}

export default AssistantPage;
