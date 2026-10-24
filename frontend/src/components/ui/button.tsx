import type { ButtonHTMLAttributes } from "react";

type ButtonVariant = "default" | "outline" | "ghost";
type ButtonSize = "default" | "icon";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
}

export function Button({
  className = "",
  size = "default",
  variant = "default",
  ...props
}: ButtonProps) {
  const variants: Record<ButtonVariant, string> = {
    default: "bg-primary text-primary-foreground hover:bg-primary/90",
    outline: "border bg-background hover:bg-muted",
    ghost: "hover:bg-muted",
  };
  const sizes: Record<ButtonSize, string> = {
    default: "h-10 px-4 py-2",
    icon: "size-10",
  };
  return (
    <button
      className={`inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors disabled:pointer-events-none disabled:opacity-50 ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    />
  );
}
