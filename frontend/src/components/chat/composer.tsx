"use client";

import {
  type ChangeEvent,
  type FormEvent,
  type KeyboardEvent,
  useEffect,
  useRef,
} from "react";
import { ArrowUp, CornerDownLeft } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface ComposerProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  disabled?: boolean;
  placeholder?: string;
}

export function Composer({
  value,
  onChange,
  onSubmit,
  disabled = false,
  placeholder = "Ask your assistant anything…",
}: ComposerProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    textarea.style.height = "auto";
    textarea.style.height = `${Math.min(textarea.scrollHeight, 180)}px`;
  }, [value]);

  function submit(event?: FormEvent<HTMLFormElement>) {
    event?.preventDefault();
    if (!disabled && value.trim()) onSubmit();
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
      event.preventDefault();
      submit();
    }
  }

  function handleChange(event: ChangeEvent<HTMLTextAreaElement>) {
    onChange(event.target.value);
  }

  return (
    <div className="sticky bottom-0 z-10 border-t bg-background/85 px-4 py-4 backdrop-blur-xl">
      <form className="mx-auto w-full max-w-3xl" onSubmit={submit}>
        <div className="relative rounded-2xl border bg-card shadow-lg shadow-black/[0.03] transition-colors focus-within:border-primary/50 focus-within:ring-2 focus-within:ring-primary/10">
          <Textarea
            aria-label="Message assistant"
            className="min-h-14 resize-none border-0 bg-transparent px-4 py-4 pr-14 shadow-none focus-visible:ring-0"
            disabled={disabled}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            ref={textareaRef}
            rows={1}
            value={value}
          />
          <Button
            aria-label="Send message"
            className="absolute bottom-2.5 right-2.5 size-9 rounded-xl"
            disabled={disabled || !value.trim()}
            size="icon"
            type="submit"
          >
            <ArrowUp className="size-4" aria-hidden="true" />
          </Button>
        </div>
        <div className="mt-2 flex items-center justify-center gap-1.5 text-[11px] text-muted-foreground">
          <CornerDownLeft className="size-3" aria-hidden="true" />
          <span>
            Press <kbd className="font-semibold">Ctrl</kbd> or{" "}
            <kbd className="font-semibold">⌘</kbd> + Enter to send
          </span>
        </div>
      </form>
    </div>
  );
}
