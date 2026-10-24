import { Sparkles } from "lucide-react";

import type { Agent } from "@/lib/api";

interface EmptyStateProps {
  agent: Agent;
  onPromptSelect: (prompt: string) => void;
}

export function EmptyState({ agent, onPromptSelect }: EmptyStateProps) {
  const prompts = [
    `Help me get started with ${agent.name.replace(" Agent", "").toLowerCase()}.`,
    "Give me a practical plan for today.",
    "What can you help me with?",
  ];

  return (
    <section className="mx-auto flex h-full w-full max-w-3xl flex-col items-center justify-center px-4 py-12 text-center">
      <div className="flex size-14 items-center justify-center rounded-2xl bg-primary/10 text-2xl">
        {agent.icon}
      </div>
      <p className="mt-5 text-sm font-medium text-primary">{agent.name}</p>
      <h2 className="mt-2 text-3xl font-semibold tracking-tight">
        How can I help?
      </h2>
      <p className="mt-3 max-w-lg text-sm leading-6 text-muted-foreground">
        {agent.tagline}
      </p>
      <div className="mt-8 grid w-full gap-3 sm:grid-cols-3">
        {prompts.map((prompt) => (
          <button
            className="rounded-xl border bg-card p-4 text-left text-sm shadow-sm transition-colors hover:border-primary/40 hover:bg-primary/[0.03]"
            key={prompt}
            onClick={() => onPromptSelect(prompt)}
            type="button"
          >
            <Sparkles className="mb-3 size-4 text-primary" aria-hidden="true" />
            {prompt}
          </button>
        ))}
      </div>
    </section>
  );
}
