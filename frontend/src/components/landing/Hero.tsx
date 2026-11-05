import { ArrowRight, Sparkles, Terminal, Zap, CheckCircle2 } from "lucide-react";

interface HeroProps {
  onLaunchApp: () => void;
}

export function Hero({ onLaunchApp }: HeroProps) {
  return (
    <section className="relative overflow-hidden px-4 pb-16 pt-32 sm:px-6 sm:pt-40 lg:px-8 lg:pb-24 lg:pt-44">
      {/* Ambient Light Effects */}
      <div className="pointer-events-none absolute inset-0 -top-24 flex justify-center">
        <div className="h-[520px] w-[800px] rounded-full bg-[radial-gradient(ellipse,rgba(104,64,255,0.18),transparent_65%)] blur-3xl" />
      </div>
      <div className="pointer-events-none absolute right-12 top-48 hidden lg:block">
        <div className="h-[320px] w-[320px] rounded-full bg-[radial-gradient(ellipse,rgba(161,255,98,0.12),transparent_70%)] blur-2xl" />
      </div>

      <div className="relative mx-auto max-w-5xl text-center">
        {/* Pill Badge */}
        <div className="animate-osmo-up mb-8 flex justify-center">
          <div className="osmo-mono-badge inline-flex items-center gap-2 border border-[#312E2E] bg-[#201D1D] text-[#A1FF62] shadow-[0_0_24px_rgba(161,255,98,0.15)]">
            <Sparkles className="size-3.5 fill-current" />
            <span>OmniDesk · 8 Specialized AI Desks · Grounded Results</span>
          </div>
        </div>

        {/* Clear, High-Impact Headline */}
        <h1 className="animate-osmo-up-delay-1 font-hafferXh text-4xl font-normal leading-[1.05] tracking-tight text-[#F4F4F4] sm:text-6xl md:text-7xl lg:text-8xl">
          Your Intelligent{" "}
          <span className="block mt-2 text-[#A1FF62]">
            Multi-Agent Assistant
          </span>
        </h1>

        {/* Meaningful Product Subtitle */}
        <p className="animate-osmo-up-delay-2 mx-auto mt-7 max-w-2xl text-base leading-7 text-[#B8B8B8] sm:text-lg sm:leading-8">
          Stop struggling with generic AI chatbots that guess numbers and hallucinate plans.
          OmniDesk routes every prompt to 8 dedicated domain agents—combining Google Gemini
          reasoning with deterministic Python algorithms for exact mathematical accuracy.
        </p>

        {/* Action Buttons */}
        <div className="animate-osmo-up-delay-3 mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <button
            className="btn-osmo-purple text-base px-8 py-3.5"
            onClick={onLaunchApp}
            type="button"
          >
            <Zap className="size-4 fill-current text-[#A1FF62]" />
            Start a focused session
          </button>
          <a
            className="btn-osmo-stroke text-sm px-7 py-3 text-[#F4F4F4]"
            href="#desks"
          >
            Explore 8 Desks
            <ArrowRight className="size-4 text-[#817F7F]" />
          </a>
        </div>

        {/* Key Value Highlights */}
        <div className="animate-osmo-up-delay-3 mt-12 flex flex-wrap items-center justify-center gap-6 text-xs text-[#817F7F]">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="size-4 text-[#A1FF62]" />
            <span>FastAPI & LangChain Backend</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="size-4 text-[#A1FF62]" />
            <span>Exact Mathematical Calculations</span>
          </div>
          <div className="flex items-center gap-2">
            <CheckCircle2 className="size-4 text-[#A1FF62]" />
            <span>Context-Aware Memory System</span>
          </div>
        </div>
      </div>

      {/* Featured Live Preview Mockup */}
      <div className="animate-osmo-up-delay-4 mx-auto mt-16 max-w-4xl sm:mt-20">
        <div className="osmo-card p-3 shadow-2xl backdrop-blur-xl">
          <div className="overflow-hidden rounded-lg border border-[#312E2E] bg-[#151313]">
            {/* Window bar */}
            <div className="flex items-center justify-between border-b border-[#312E2E] bg-[#201D1D] px-4 py-3">
              <div className="flex gap-2">
                <span className="size-2.5 rounded-full bg-[#F84131]" />
                <span className="size-2.5 rounded-full bg-[#393636]" />
                <span className="size-2.5 rounded-full bg-[#A1FF62]" />
              </div>
              <div className="flex items-center gap-2 rounded-full border border-[#312E2E] bg-[#151313] px-3.5 py-1 text-[11px] font-hafferMono text-[#817F7F]">
                <Terminal className="size-3 text-[#A1FF62]" />
                <span>omnidesk.local :8001 / finance</span>
              </div>
              <div className="flex items-center gap-1.5 text-[11px] font-medium text-[#A1FF62]">
                <span className="size-2 rounded-full bg-[#A1FF62] animate-pulse" />
                Deterministic Engine Active
              </div>
            </div>

            {/* Inner App Preview Grid */}
            <div className="flex min-h-[300px] sm:min-h-[340px]">
              {/* Sidebar */}
              <div className="hidden w-52 shrink-0 border-r border-[#312E2E] bg-[#1A1818] p-3 sm:block">
                <div className="mb-2 px-2 pt-1 font-hafferMono text-[10px] uppercase tracking-wider text-[#817F7F]">
                  Domain Specialists
                </div>
                {[
                  { name: "Weather Desk", color: "#6840FF" },
                  { name: "Travel Desk", color: "#A1FF62" },
                  { name: "Finance Desk", color: "#A1FF62", active: true },
                  { name: "Planning Desk", color: "#B8B8B8" },
                  { name: "Career Desk", color: "#6840FF" },
                  { name: "Health Desk", color: "#A1FF62" },
                  { name: "Kitchen Desk", color: "#F84131" },
                  { name: "Study Desk", color: "#B8B8B8" },
                ].map((item) => (
                  <div
                    className={`mb-1 flex items-center gap-2 rounded-md px-2.5 py-1.5 text-xs transition-colors ${
                      item.active
                        ? "bg-[#201D1D] font-medium text-[#A1FF62] border border-[#312E2E]"
                        : "text-[#817F7F]"
                    }`}
                    key={item.name}
                  >
                    <span className="size-1.5 rounded-full" style={{ backgroundColor: item.color }} />
                    {item.name}
                  </div>
                ))}
              </div>

              {/* Chat View */}
              <div className="flex flex-1 flex-col justify-between p-4 sm:p-6">
                <div className="space-y-3.5">
                  <div className="flex items-center justify-between">
                    <span className="rounded-full border border-[#312E2E] bg-[#201D1D] px-3 py-1 text-xs text-[#A1FF62] font-hafferMono">
                      ⚡ Finance Specialist Desk
                    </span>
                    <span className="text-[11px] text-[#817F7F]">Python calculate_emi tool</span>
                  </div>

                  <div className="ml-auto max-w-[80%] rounded-xl bg-[#201D1D] border border-[#312E2E] px-4 py-2.5 text-xs text-[#F4F4F4]">
                    Calculate monthly EMI for a $60,000 auto loan at 8.25% interest over 5 years.
                  </div>

                  <div className="max-w-[95%] rounded-xl bg-[#201D1D] border border-[#312E2E] p-4 text-xs text-[#F4F4F4]">
                    <div className="mb-2.5 flex items-center gap-2">
                      <span className="rounded-full bg-[#A1FF62]/20 px-2 py-0.5 text-[10px] font-bold text-[#A1FF62]">
                        ✓ Tool Executed: calculate_emi
                      </span>
                      <span className="text-[10px] text-[#817F7F]">0.38s latency · Exact math</span>
                    </div>
                    <div className="grid grid-cols-2 gap-3 rounded-lg bg-[#151313] p-3 border border-[#312E2E]">
                      <div>
                        <span className="text-[10px] text-[#817F7F] uppercase tracking-wider">Monthly Payment</span>
                        <p className="font-hafferMono text-base font-bold text-[#A1FF62] mt-0.5">$1,223.82</p>
                      </div>
                      <div>
                        <span className="text-[10px] text-[#817F7F] uppercase tracking-wider">Total Interest</span>
                        <p className="font-hafferMono text-base font-bold text-[#F4F4F4] mt-0.5">$13,429.20</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-4 flex items-center justify-between rounded-full border border-[#312E2E] bg-[#201D1D] px-4 py-2.5 text-xs text-[#817F7F]">
                  <span>Ask any calculation, travel plan, recipe, or agenda…</span>
                  <div className="flex size-6 items-center justify-center rounded-full bg-[#6840FF] text-[#F4F4F4]">
                    <Zap className="size-3 fill-current text-[#A1FF62]" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
