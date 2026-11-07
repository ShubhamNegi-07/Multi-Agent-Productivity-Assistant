"use client";

import {
  type ChangeEvent,
  type FormEvent,
  type KeyboardEvent,
  useEffect,
  useRef,
} from "react";
import { CornerDownLeft, Plus, Zap } from "lucide-react";

import type { Agent } from "@/lib/api";
import { AgentIcon } from "@/components/assistant/agent-icon";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface ComposerProps {
  agent: Agent | null;
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  disabled?: boolean;
  placeholder?: string;
}

export function Composer({
  agent,
  value,
  onChange,
  onSubmit,
  disabled = false,
  placeholder = "Describe the work in front of you…",
}: ComposerProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = "auto";
    textarea.style.height = `${Math.min(textarea.scrollHeight, 160)}px`;
  }, [value]);

  function submit(event?: FormEvent<HTMLFormElement>) {
    event?.preventDefault();
    if (!disabled && value.trim()) onSubmit();
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (
      event.key === "Enter" &&
      !event.shiftKey &&
      !event.nativeEvent.isComposing
    ) {
      event.preventDefault();
      submit();
    }
  }

  function handleChange(event: ChangeEvent<HTMLTextAreaElement>) {
    onChange(event.target.value);
  }

  return (
    <div className="pointer-events-none absolute inset-x-0 bottom-5 z-50 flex justify-center px-4 sm:bottom-6">
      <form className="pointer-events-auto w-full max-w-3xl font-hafferXh" onSubmit={submit}>
        <div className="relative mx-auto w-full rounded-2xl border border-[#312E2E] bg-[#201D1D]/95 shadow-[0_24px_60px_-16px_rgba(0,0,0,0.7)] backdrop-blur-2xl">
          {/* Top metadata strip */}
          <div className="flex w-full items-center justify-between border-b border-[#312E2E] px-4 pb-2 pt-2.5 text-xs text-[#817F7F]">
            <div className="inline-flex items-center gap-1.5 rounded-full bg-[#A1FF62]/10 px-3 py-1 font-hafferMono text-[11px] font-semibold text-[#A1FF62]">
              {agent ? <AgentIcon agent={agent} className="size-3" /> : <Plus className="size-3" />}
              {agent?.name ?? "Choose a desk"}
            </div>
            <span className="inline-flex items-center gap-1.5 text-[11px] text-[#817F7F]">
              <span className="size-1.5 rounded-full bg-[#A1FF62]" />
              Deterministic Pipeline Active
            </span>
          </div>

          {/* Text input area */}
          <div className="relative flex min-h-[64px] w-full items-center px-4 py-3">
            <Textarea
              aria-label="Message assistant"
              className="min-h-[26px] max-h-[160px] w-full resize-none rounded-md !border-0 bg-transparent py-1.5 pr-14 font-hafferXh text-sm leading-6 text-[#F4F4F4] shadow-none placeholder:text-[#817F7F] outline-none focus:!border-0 focus:outline-none focus:ring-0 focus-visible:!outline-none focus-visible:ring-0"
              data-gramm="false"
              disabled={disabled}
              onChange={handleChange}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              ref={textareaRef}
              rows={1}
              spellCheck={false}
              value={value}
            />
            <Button
              aria-label="Send message"
              className="absolute right-4 top-1/2 flex size-8 -translate-y-1/2 items-center justify-center rounded-full bg-[#A1FF62] text-[#201D1D] shadow-sm transition-all duration-200 hover:scale-105 active:scale-95 disabled:opacity-30"
              disabled={disabled || !value.trim()}
              size="icon"
              type="submit"
            >
              <Zap className="size-3.5 fill-current" aria-hidden="true" />
            </Button>
          </div>

          {/* Bottom hint */}
          <div className="flex w-full items-center justify-between px-4 pb-2.5 text-[10px] text-[#817F7F]">
            <span>Enter to send · Shift+Enter for new line</span>
            <span className="hidden items-center gap-1 font-hafferMono sm:inline-flex">
              <CornerDownLeft className="size-2.5 text-[#A1FF62]" />
              <kbd className="rounded border border-[#312E2E] bg-[#151313] px-1.5 py-0.5 text-[9px] text-[#F4F4F4]">Return</kbd>
            </span>
          </div>
        </div>
      </form>
    </div>
  );
}
