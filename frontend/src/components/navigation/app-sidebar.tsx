import { useEffect, useMemo, useState } from "react";
import {
  ArrowLeft,
  CirclePlus,
  LoaderCircle,
  PanelLeftClose,
  RotateCw,
  Search,
  X,
  Zap,
} from "lucide-react";

import { ApiError, getAgents, type Agent } from "@/lib/api";
import { AgentIcon } from "@/components/assistant/agent-icon";
import { OmniLogo } from "@/components/brand/OmniLogo";
import { Tooltip, TooltipProvider } from "@/components/ui/tooltip";

interface AppSidebarProps {
  activeAgentId: string;
  onAgentChange: (agent: Agent) => void;
  onNewChat: () => void;
  isProcessing?: boolean;
  onAgentsLoaded?: (agents: Agent[]) => void;
  onAgentsError?: (message: string) => void;
  onBackToLanding?: () => void;
}

export function AppSidebar({
  activeAgentId,
  onAgentChange,
  onNewChat,
  isProcessing = false,
  onAgentsLoaded,
  onAgentsError,
  onBackToLanding,
}: AppSidebarProps) {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [retryKey, setRetryKey] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    let mounted = true;

    setIsLoading(true);
    getAgents(controller.signal)
      .then((nextAgents) => {
        if (!mounted) return;
        setAgents(nextAgents);
        setError(null);
        onAgentsLoaded?.(nextAgents);
      })
      .catch((reason: unknown) => {
        if (reason instanceof DOMException && reason.name === "AbortError") return;
        if (!mounted) return;
        const message =
          reason instanceof ApiError
            ? reason.message
            : "Unable to connect to the workspace API.";
        setError(message);
        onAgentsError?.(message);
      })
      .finally(() => {
        if (mounted) setIsLoading(false);
      });

    return () => {
      mounted = false;
      controller.abort();
    };
  }, [onAgentsError, onAgentsLoaded, retryKey]);

  const filteredAgents = useMemo(
    () =>
      agents.filter((agent) =>
        agent.name.toLowerCase().includes(query.trim().toLowerCase()),
      ),
    [agents, query],
  );

  return (
    <aside
      className={[
        "flex h-dvh shrink-0 flex-col border-r border-[#312E2E] bg-[#151313] text-[#F4F4F4]",
        isCollapsed ? "w-16 items-center px-0" : "w-[264px] px-3",
      ].join(" ")}
    >
      {/* Brand Header */}
      <div
        className={[
          "flex w-full items-center px-2 py-3 pt-4",
          isCollapsed ? "justify-center" : "justify-between",
        ].join(" ")}
      >
        <div className={isCollapsed ? "flex items-center justify-center" : "flex min-w-0 shrink-0 items-center gap-2.5"}>
          <OmniLogo compact />
          {!isCollapsed && (
            <div>
              <p className="font-hafferVf text-sm font-bold tracking-tight text-[#F4F4F4]">OmniDesk</p>
              <p className="font-hafferMono text-[10px] uppercase text-[#817F7F]">8 AI Specialists</p>
            </div>
          )}
        </div>
        {!isCollapsed && (
          <button
            aria-label="Collapse sidebar"
            className="ml-auto hidden size-7 shrink-0 items-center justify-center rounded-lg text-[#817F7F] transition-colors hover:bg-[#201D1D] hover:text-[#F4F4F4] md:inline-flex"
            onClick={() => setIsCollapsed(true)}
            title="Collapse sidebar"
            type="button"
          >
            <PanelLeftClose className="size-4" />
          </button>
        )}
      </div>

      {/* Back to Landing */}
      {onBackToLanding && !isCollapsed && (
        <button
          className="mx-1 mt-1 flex items-center gap-2 rounded-full border border-[#312E2E] bg-[#201D1D] px-3 py-1.5 text-xs text-[#B8B8B8] transition-all hover:border-[#6840FF] hover:text-[#F4F4F4]"
          onClick={onBackToLanding}
          type="button"
        >
          <ArrowLeft className="size-3" />
          <span>Back to Landing</span>
        </button>
      )}

      <div className="flex flex-col overflow-hidden pb-4 pt-4">
        {/* New Conversation Button (Pill 51.2px) */}
        <button
          className={[
            "flex h-9 items-center gap-2 rounded-full border border-[#A1FF62]/40 bg-[#A1FF62]/10 text-xs font-semibold text-[#A1FF62] transition-all duration-200 hover:bg-[#A1FF62] hover:text-[#201D1D]",
            isCollapsed ? "mx-auto size-9 justify-center" : "px-3.5",
          ].join(" ")}
          disabled={isProcessing}
          onClick={onNewChat}
          title="New Conversation"
          type="button"
        >
          <CirclePlus className="size-3.5" />
          {!isCollapsed && <span>New Conversation</span>}
        </button>

        {/* Search Input */}
        {!isCollapsed && (
          <label className="mt-3.5 flex h-8 items-center gap-2 rounded-full border border-[#312E2E] bg-[#201D1D] px-3 text-[#817F7F] focus-within:border-[#6840FF]">
            <Search className="size-3 shrink-0" aria-hidden="true" />
            <input
              aria-label="Search 8 desks"
              className="min-w-0 flex-1 bg-transparent text-xs outline-none placeholder:text-[#817F7F] text-[#F4F4F4]"
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search 8 desks…"
              value={query}
            />
            {query && (
              <button
                aria-label="Clear filter"
                className="inline-flex size-4 shrink-0 items-center justify-center rounded text-[#817F7F] hover:text-[#F4F4F4]"
                onClick={() => setQuery("")}
                type="button"
              >
                <X className="size-3" aria-hidden="true" />
              </button>
            )}
          </label>
        )}

        {/* Specialist Desks Section */}
        <div className="scrollbar-hidden mt-5 min-h-0 overflow-y-auto">
          <>
            <TooltipProvider>
              <div className="mt-2 space-y-1 py-1">
                {isLoading && (
                  <p className="flex items-center gap-2 px-2 py-3 text-xs text-[#817F7F]">
                    <LoaderCircle className="size-3.5 animate-spin text-[#A1FF62]" />
                    {!isCollapsed && "Loading desks…"}
                  </p>
                )}
                {error && !isCollapsed && (
                  <div className="m-1 rounded-lg border border-[#F84131]/30 bg-[#F84131]/10 p-2.5">
                    <p className="text-xs text-[#F84131]">{error}</p>
                    <button
                      className="mt-2 inline-flex items-center gap-1.5 text-[11px] font-medium text-[#F4F4F4] hover:text-[#A1FF62]"
                      onClick={() => setRetryKey((current) => current + 1)}
                      type="button"
                    >
                      <RotateCw className="size-3" /> Retry
                    </button>
                  </div>
                )}
                {filteredAgents.map((agent) => {
                  const isActive = activeAgentId === agent.id;
                  const workspaceButton = (
                    <button
                      className={[
                        "group flex w-full items-center gap-2.5 rounded-xl py-2 text-left text-xs font-medium transition-all duration-200",
                        isCollapsed ? "justify-center px-0 min-h-10" : "px-3 min-h-9",
                        isActive
                          ? "border border-[#A1FF62]/40 bg-[#A1FF62]/15 text-[#F4F4F4] shadow-[0_0_16px_rgba(161,255,98,0.2)]"
                          : "border border-transparent text-[#B8B8B8] hover:bg-[#201D1D] hover:text-[#F4F4F4]",
                      ].join(" ")}
                      disabled={isProcessing}
                      key={agent.id}
                      onClick={() => onAgentChange(agent)}
                      type="button"
                    >
                      <span className={`flex size-6 shrink-0 items-center justify-center rounded-lg transition-colors ${
                        isActive
                          ? "bg-[#A1FF62] text-[#201D1D]"
                          : "bg-[#201D1D] text-[#817F7F] group-hover:text-[#A1FF62]"
                      }`}>
                        <AgentIcon agent={agent} className="size-3.5" aria-hidden="true" />
                      </span>
                      {!isCollapsed && (
                        <>
                          <span className="min-w-0 flex-1 truncate">{agent.name.replace(" Desk", "")}</span>
                          {isActive && (
                            <Zap className="size-3 fill-current text-[#A1FF62]" />
                          )}
                        </>
                      )}
                    </button>
                  );
                  return isCollapsed ? (
                    <Tooltip content={agent.name} key={agent.id}>
                      {workspaceButton}
                    </Tooltip>
                  ) : (
                    workspaceButton
                  );
                })}
              </div>
            </TooltipProvider>
          </>
        </div>
      </div>
    </aside>
  );
}
