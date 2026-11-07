"use client";

import { useState } from "react";
import { Check, Clipboard, Zap } from "lucide-react";

import type { Agent, ChatMessage } from "@/lib/api";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { AgentIcon } from "@/components/assistant/agent-icon";

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
      className="mx-auto flex w-full max-w-3xl flex-col space-y-5 px-4 py-4"
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
    <div className="flex justify-end px-1">
      <div className="max-w-[80%] rounded-2xl rounded-tr-sm bg-[#201D1D] border border-[#312E2E] px-4 py-3">
        <p className="whitespace-pre-wrap text-sm leading-6 text-[#F4F4F4]">
          {message.content}
        </p>
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
    <div className="group flex items-start gap-3.5">
      <Avatar className="mt-0.5 size-7 shrink-0 rounded-lg">
        <AvatarFallback className="rounded-lg bg-[#201D1D] border border-[#312E2E] text-[#A1FF62]">
          <AgentIcon agent={activeAgent} className="size-3.5" aria-hidden="true" />
        </AvatarFallback>
      </Avatar>
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-center gap-x-2 gap-y-1">
          <span className="font-hafferVf text-xs font-bold leading-5 text-[#F4F4F4]">
            {message.agent || activeAgent.name}
          </span>
          {message.isError && (
            <span className="rounded-full bg-[#F84131]/15 px-2 py-0.5 font-hafferMono text-[10px] font-semibold text-[#F84131]">Error</span>
          )}
          {message.elapsedMs !== undefined && (
            <span className="inline-flex items-center gap-1 rounded-full border border-[#312E2E] bg-[#151313] px-2 py-0.5 font-hafferMono text-[10px] tabular-nums text-[#817F7F]">
              <Zap className="size-2.5 text-[#A1FF62]" />
              {(message.elapsedMs / 1000).toFixed(2)}s
            </span>
          )}

          <Button
            aria-label={copied ? "Copied response" : "Copy response"}
            className="size-6 text-[#817F7F] opacity-0 transition-opacity duration-150 group-hover:opacity-100 hover:text-[#F4F4F4]"
            onClick={copyMessage}
            size="icon"
            variant="ghost"
          >
            {copied ? (
              <Check className="size-3 text-[#A1FF62]" aria-hidden="true" />
            ) : (
              <Clipboard className="size-3" aria-hidden="true" />
            )}
          </Button>
        </div>
        <div className="mt-2 rounded-xl bg-[#201D1D] border border-[#312E2E] p-4">
          <p
            className={[
              "whitespace-pre-wrap text-sm leading-7 text-[#F4F4F4]/90",
              message.isError ? "text-[#F84131]" : "",
            ].join(" ")}
          >
            {message.content}
          </p>
        </div>
      </div>
    </div>
  );
}

function TypingIndicator({ agent }: { agent: Agent }) {
  return (
    <div className="flex items-center gap-3 px-1 text-sm text-[#817F7F]" role="status">
      <Avatar className="size-7 rounded-lg">
        <AvatarFallback className="rounded-lg bg-[#201D1D] border border-[#312E2E] text-[#A1FF62]">
          <AgentIcon agent={agent} className="size-3.5" aria-hidden="true" />
        </AvatarFallback>
      </Avatar>
      <div className="flex items-center gap-2">
        <span
          aria-hidden="true"
          className="thinking-spinner size-3.5 shrink-0 rounded-full border-2 border-[#A1FF62]/30 border-t-[#A1FF62]"
        />
        <span className="text-xs text-[#817F7F]">
          {agent.name} is executing tools…
        </span>
      </div>
    </div>
  );
}
