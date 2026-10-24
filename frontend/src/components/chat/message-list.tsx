"use client";

import { useState } from "react";
import { Check, Clipboard, Loader2 } from "lucide-react";

import type { Agent, ChatMessage } from "@/lib/api";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

export interface DisplayMessage extends ChatMessage {
  id: string;
  elapsedMs?: number;
  isError?: boolean;
}

interface MessageListProps {
  messages: DisplayMessage[];
  activeAgent: Agent;
  isProcessing?: boolean;
}

export function MessageList({
  messages,
  activeAgent,
  isProcessing = false,
}: MessageListProps) {
  return (
    <div
      aria-live="polite"
      className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-4 py-8"
      role="log"
    >
      {messages.map((message) =>
        message.role === "user" ? (
          <UserMessage key={message.id} message={message} />
        ) : (
          <AgentMessage
            activeAgent={activeAgent}
            key={message.id}
            message={message}
          />
        ),
      )}
      {isProcessing && <TypingIndicator agent={activeAgent} />}
    </div>
  );
}

function UserMessage({ message }: { message: DisplayMessage }) {
  return (
    <div className="flex justify-end">
      <div className="max-w-[85%] rounded-2xl rounded-br-md bg-primary px-4 py-3 text-sm leading-6 text-primary-foreground shadow-sm">
        <p className="whitespace-pre-wrap">{message.content}</p>
      </div>
    </div>
  );
}

function AgentMessage({
  activeAgent,
  message,
}: {
  activeAgent: Agent;
  message: DisplayMessage;
}) {
  const [copied, setCopied] = useState(false);

  async function copyMessage() {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1600);
    } catch {
      setCopied(false);
    }
  }

  return (
    <div className="flex items-start gap-3">
      <Avatar className="mt-1 size-8 shrink-0 rounded-lg">
        <AvatarFallback className="rounded-lg bg-primary/10 text-base">
          {activeAgent.icon}
        </AvatarFallback>
      </Avatar>
      <Card
        className={[
          "min-w-0 flex-1 shadow-sm",
          message.isError ? "border-destructive/30 bg-destructive/5" : "",
        ].join(" ")}
      >
        <CardHeader className="flex-row items-center gap-2 space-y-0 border-b px-4 py-3">
          <span className="text-sm font-semibold">
            {message.agent || activeAgent.name}
          </span>
          {message.isError && (
            <span className="text-xs font-medium text-destructive">Error</span>
          )}
          {message.elapsedMs !== undefined && (
            <span className="ml-auto text-xs tabular-nums text-muted-foreground">
              {(message.elapsedMs / 1000).toFixed(2)}s
            </span>
          )}
        </CardHeader>
        <CardContent className="group relative px-4 py-4">
          <p className="whitespace-pre-wrap text-sm leading-7">{message.content}</p>
          <Button
            aria-label={copied ? "Copied response" : "Copy response"}
            className="absolute right-2 top-2 opacity-0 transition-opacity group-hover:opacity-100 focus-visible:opacity-100"
            onClick={copyMessage}
            size="icon"
            variant="ghost"
          >
            {copied ? (
              <Check className="size-4 text-emerald-600" aria-hidden="true" />
            ) : (
              <Clipboard className="size-4" aria-hidden="true" />
            )}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

function TypingIndicator({ agent }: { agent: Agent }) {
  return (
    <div className="flex items-center gap-3" role="status">
      <Avatar className="size-8 rounded-lg">
        <AvatarFallback className="rounded-lg bg-primary/10 text-base">
          {agent.icon}
        </AvatarFallback>
      </Avatar>
      <div className="flex items-center gap-2 rounded-xl border bg-card px-4 py-3 text-sm text-muted-foreground shadow-sm">
        <Loader2 className="size-4 animate-spin" aria-hidden="true" />
        {agent.name} is thinking…
      </div>
    </div>
  );
}
