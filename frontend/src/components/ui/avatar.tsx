import type { HTMLAttributes } from "react";

export function Avatar({ className = "", ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={`relative flex shrink-0 overflow-hidden ${className}`} {...props} />;
}

export function AvatarFallback({
  className = "",
  ...props
}: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={`flex size-full items-center justify-center ${className}`}
      {...props}
    />
  );
}
