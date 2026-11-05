interface OmniLogoProps {
  compact?: boolean;
}

export function OmniLogo({ compact = false }: OmniLogoProps) {
  return (
    <div className={compact ? "flex size-9 items-center justify-center" : "flex items-center gap-3"}>
      <svg
        aria-label="OmniDesk logo"
        className={compact ? "size-9" : "size-10"}
        viewBox="0 0 40 40"
        role="img"
      >
        <defs>
          <linearGradient id="omni-logo-gradient" x1="4" y1="4" x2="36" y2="36">
            <stop stopColor="#A1FF62" />
            <stop offset="1" stopColor="#6840FF" />
          </linearGradient>
          <linearGradient id="omni-core-gradient" x1="14" y1="14" x2="26" y2="26">
            <stop stopColor="#A1FF62" />
            <stop offset="1" stopColor="#6840FF" />
          </linearGradient>
        </defs>
        <circle cx="20" cy="20" r="17" fill="#201D1D" stroke="#6840FF" strokeOpacity="0.85" strokeWidth="1.5" />
        <ellipse cx="20" cy="20" rx="6.4" ry="12.2" fill="none" stroke="url(#omni-logo-gradient)" strokeWidth="2.8" transform="rotate(45 20 20)" />
        <ellipse cx="20" cy="20" rx="6.4" ry="12.2" fill="none" stroke="url(#omni-logo-gradient)" strokeWidth="2.8" transform="rotate(-45 20 20)" />
        <circle cx="20" cy="20" r="3.1" fill="#201D1D" stroke="#F4F4F4" strokeWidth="1.5" />
        <circle cx="20" cy="5.2" r="1.8" fill="#A1FF62" />
        <circle cx="34.8" cy="20" r="1.8" fill="#6840FF" />
        <circle cx="20" cy="34.8" r="1.8" fill="#A1FF62" />
        <circle cx="5.2" cy="20" r="1.8" fill="#6840FF" />
      </svg>
      {!compact && (
        <div className="flex flex-col">
          <span className="font-hafferXh text-lg font-bold tracking-tight text-[#F4F4F4]">OmniDesk</span>
        </div>
      )}
    </div>
  );
}
