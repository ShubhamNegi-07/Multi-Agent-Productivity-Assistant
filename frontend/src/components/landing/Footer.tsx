import { ArrowRight, Zap } from "lucide-react";

interface FooterProps {
  onLaunchApp: () => void;
}

export function CtaBanner({ onLaunchApp }: FooterProps) {
  return (
    <section className="bg-[#151313] px-4 py-20 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-4xl">
        <div className="osmo-card relative overflow-hidden px-6 py-14 text-center sm:px-14 sm:py-18">
          {/* Ambient Glow */}
          <div className="pointer-events-none absolute inset-0 flex justify-center">
            <div className="h-full w-full rounded-2xl bg-[radial-gradient(ellipse_at_center,rgba(104,64,255,0.18),transparent_70%)]" />
          </div>

          <div className="relative z-10">
            <div className="osmo-mono-badge mx-auto mb-4 inline-flex items-center gap-1.5 border border-[#312E2E] bg-[#151313] text-[#A1FF62]">
              Start Working With Clarity
            </div>
            <h2 className="font-hafferXh text-3xl font-normal tracking-tight text-[#F4F4F4] sm:text-5xl">
              Supercharge Your Workflow With OmniDesk
            </h2>
            <p className="mx-auto mt-4 max-w-lg text-sm leading-6 text-[#B8B8B8]">
              Eight dedicated specialists for finance, travel, planning, career, health, kitchen,
              and study. Powered by verified Python tools and Google Gemini reasoning.
            </p>

            <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <button
                className="btn-osmo-purple text-base px-8 py-3.5"
                onClick={onLaunchApp}
                type="button"
              >
                <Zap className="size-4 fill-current text-[#A1FF62]" />
                Bring your work into focus
                <ArrowRight className="size-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export function Footer() {
  return (
    <footer className="border-t border-[#312E2E] bg-[#151313] px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-6 sm:flex-row">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="flex size-7 items-center justify-center rounded-full bg-[#6840FF] text-[#F4F4F4] font-bold text-xs">
            A
          </div>
          <span className="font-hafferVf text-sm font-semibold tracking-tight text-[#F4F4F4]">
            OmniDesk
          </span>
          <span className="text-xs text-[#817F7F]">
            · Multi-Agent Workspace
          </span>
        </div>

        {/* Status & Links */}
        <div className="flex flex-wrap items-center gap-6">
          <div className="flex items-center gap-2 rounded-full border border-[#312E2E] bg-[#201D1D] px-3.5 py-1 text-xs text-[#817F7F]">
            <span className="size-2 rounded-full bg-[#A1FF62] animate-pulse" />
            <span className="text-[#F4F4F4]">FastAPI & 8 Desks Active</span>
          </div>

          <span className="text-xs text-[#817F7F]">
            © {new Date().getFullYear()} OmniDesk. Built with FastAPI & LangChain.
          </span>
        </div>
      </div>
    </footer>
  );
}
