import type { HTMLAttributes } from "react";

function part(className: string, props: HTMLAttributes<HTMLDivElement>) {
  return <div className={className} {...props} />;
}

export function Card({ className = "", ...props }: HTMLAttributes<HTMLDivElement>) {
  return part(`rounded-xl border bg-card text-card-foreground ${className}`, props);
}
export function CardHeader({ className = "", ...props }: HTMLAttributes<HTMLDivElement>) {
  return part(`p-6 ${className}`, props);
}
export function CardContent({ className = "", ...props }: HTMLAttributes<HTMLDivElement>) {
  return part(`p-6 pt-0 ${className}`, props);
}
