import React from 'react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export interface GlassCardProps extends React.HTMLAttributes<HTMLDivElement> {
  hoverEffect?: boolean;
}

export function GlassCard({
  children,
  className,
  hoverEffect = false,
  ...props
}: GlassCardProps) {
  return (
    <div
      className={cn(
        "rounded-2xl border border-white/10 bg-black/40 backdrop-blur-md p-6 text-white shadow-xl transition-all duration-300",
        hoverEffect && "hover:border-indigo-500/30 hover:bg-black/60 hover:shadow-indigo-500/5",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export interface GradientButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline';
}

export function GradientButton({
  children,
  className,
  variant = 'primary',
  ...props
}: GradientButtonProps) {
  const baseStyle = "relative inline-flex items-center justify-center rounded-xl px-6 py-3 text-sm font-semibold tracking-wide transition-all duration-300 disabled:opacity-50 disabled:pointer-events-none active:scale-[0.98]";
  
  const variants = {
    primary: "bg-gradient-to-r from-violet-600 via-indigo-600 to-purple-600 text-white hover:opacity-95 shadow-[0_0_20px_rgba(99,102,241,0.3)] hover:shadow-[0_0_25px_rgba(99,102,241,0.5)]",
    secondary: "bg-white/10 text-white hover:bg-white/15 border border-white/10",
    outline: "border border-violet-500/50 bg-transparent text-violet-300 hover:bg-violet-500/10 hover:text-white"
  };

  return (
    <button
      className={cn(baseStyle, variants[variant], className)}
      {...props}
    >
      {children}
    </button>
  );
}

export function Spinner({ className }: { className?: string }) {
  return (
    <svg
      className={cn("animate-spin h-5 w-5 text-indigo-500", className)}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  );
}

export function Badge({ children, className, variant = 'info' }: { children: React.ReactNode, className?: string, variant?: 'info' | 'warning' | 'success' }) {
  const styles = {
    info: "bg-indigo-500/10 text-indigo-300 border-indigo-500/20",
    warning: "bg-amber-500/10 text-amber-300 border-amber-500/20",
    success: "bg-emerald-500/10 text-emerald-300 border-emerald-500/20"
  };

  return (
    <span className={cn("inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2", styles[variant], className)}>
      {children}
    </span>
  );
}
