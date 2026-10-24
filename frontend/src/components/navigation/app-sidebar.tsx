import { useEffect, useState } from "react";
import { Brain, Plus, Sparkles } from "lucide-react";

import { ApiError, getAgents, type Agent } from "@/lib/api";
import { Button } from "@/components/ui/button";

interface AppSidebarProps {
  agents?: Agent[];
  activeAgentId: string;
  onAgentChange: (agent: Agent) => void;
  remember: boolean;
  onRememberChange: (remember: boolean) => void;
  onNewChat: () => void;
  hasMessages?: boolean;
  isProcessing?: boolean;
  onAgentsLoaded?: (agents: Agent[]) => void;
}

export function AppSidebar({
  agents: providedAgents,
  activeAgentId,
  onAgentChange,
  remember,
  onRememberChange,
  onNewChat,
  hasMessages = false,
  isProcessing = false,
  onAgentsLoaded,
}: AppSidebarProps) {
  const [loadedAgents, setLoadedAgents] = useState<Agent[]>([]);
  const [isLoading, setIsLoading] = useState(!providedAgents);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (providedAgents) {
      setIsLoading(false);
      return;
    }

    const controller = new AbortController();
    let mounted = true;

    getAgents(controller.signal)
      .then((nextAgents) => {
        if (!mounted) return;
        setLoadedAgents(nextAgents);
        onAgentsLoaded?.(nextAgents);
      })
      .catch((reason: unknown) => {
        if (reason instanceof DOMException && reason.name === "AbortError") return;
        if (mounted) {
          setError(
            reason instanceof ApiError
              ? reason.message
              : "Unable to load specialist agents.",
          );
        }
      })
      .finally(() => {
        if (mounted) setIsLoading(false);
      });

    return () => {
      mounted = false;
      controller.abort();
    };
  }, [onAgentsLoaded, providedAgents]);

  const agents = providedAgents ?? loadedAgents;

  return (
    <aside className="flex h-dvh w-full max-w-72 flex-col border-r bg-sidebar px-3 py-4 text-sidebar-foreground">
      <div className="flex items-center gap-3 px-2 py-2">
        <div className="flex size-9 items-center justify-center rounded-xl bg-primary text-primary-foreground">
          <Sparkles className="size-4" aria-hidden="true" />
        </div>
        <div>
          <p className="text-sm font-semibold">Assistant Hub</p>
          <p className="text-xs text-muted-foreground">Your specialist team</p>
        </div>
      </div>

      <Button
        className="mt-5 w-full justify-start gap-2"
        disabled={isProcessing}
        onClick={onNewChat}
        variant={hasMessages ? "outline" : "default"}
      >
        <Plus className="size-4" aria-hidden="true" />
        New chat
      </Button>

      <div className="mt-6 flex-1 overflow-y-auto">
        <p className="px-2 text-xs font-medium uppercase tracking-wide text-muted-foreground">
          Specialists
        </p>
        <div className="mt-2 space-y-1">
          {isLoading && (
            <p className="px-2 py-3 text-sm text-muted-foreground">Loading agents…</p>
          )}
          {error && <p className="px-2 py-3 text-sm text-destructive">{error}</p>}
          {agents.map((agent) => (
            <button
              className={[
                "flex w-full items-center gap-3 rounded-lg px-3 py-2 text-left text-sm transition-colors",
                activeAgentId === agent.id
                  ? "bg-primary/10 font-medium text-primary"
                  : "hover:bg-muted",
              ].join(" ")}
              disabled={isProcessing}
              key={agent.id}
              onClick={() => onAgentChange(agent)}
              type="button"
            >
              <span className="text-base" aria-hidden="true">{agent.icon}</span>
              <span className="truncate">{agent.name}</span>
            </button>
          ))}
        </div>
      </div>

      <label className="flex cursor-pointer items-center gap-3 rounded-lg border bg-card px-3 py-3 text-sm">
        <Brain className="size-4 text-muted-foreground" aria-hidden="true" />
        <span className="flex-1">Remember context</span>
        <input
          checked={remember}
          className="size-4 accent-primary"
          onChange={(event) => onRememberChange(event.target.checked)}
          type="checkbox"
        />
      </label>
    </aside>
  );
}
