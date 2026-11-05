import { Check, Zap } from "lucide-react";

const tiers = [
  {
    name: "Specialist Desks",
    stat: "08",
    description: "Move between focused workspaces built for the decisions you make every day.",
    features: [
      "Weather, travel, finance, and planning",
      "Career, health, kitchen, and study support",
      "A clear prompt space for each domain",
      "Switch desks without losing your workflow",
    ],
    cta: "Explore the desks",
    featured: false,
  },
  {
    name: "Grounded Tools",
    stat: "Python",
    description: "Turn everyday questions into useful results with tools that handle the details.",
    features: [
      "EMI, interest, BMI, and calorie calculations",
      "Trip budgets, checklists, and itineraries",
      "Recipe scaling, conversions, and shopping lists",
      "Study plans, agendas, and structured task lists",
    ],
    cta: "See how it works",
    featured: true,
  },
  {
    name: "Your Workspace",
    stat: "Local-first",
    description: "Keep your conversations organized and bring context into the next useful step.",
    features: [
      "Optional conversation memory",
      "Bounded history for focused context",
      "Copy responses and export useful notes",
      "FastAPI backend with a responsive React UI",
    ],
    cta: "Open your workspace",
    featured: false,
  },
];

export function PricingTable() {
  return (
    <section id="platform" className="bg-[#151313] px-4 py-24 sm:px-6 lg:px-8 border-t border-[#312E2E]">
      <div className="mx-auto max-w-6xl">
        <div className="mb-14 text-center">
          <div className="osmo-mono-badge mb-3 inline-flex items-center gap-1.5 border border-[#312E2E] bg-[#201D1D] text-[#A1FF62]">
            Built for Focused Work
          </div>
          <h2 className="font-hafferXh text-3xl font-normal tracking-tight text-[#F4F4F4] sm:text-5xl">
            One Workspace. Eight Specialist Desks.
          </h2>
          <p className="mx-auto mt-4 max-w-md text-sm leading-6 text-[#B8B8B8]">
            OmniDesk brings practical AI tools into one calm workspace, so you
            can move from a question to a clear next step.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          {tiers.map((tier) => (
            <div
              className={`relative flex flex-col justify-between rounded-xl p-7 transition-all duration-200 ${
                tier.featured
                  ? "border-2 border-[#6840FF] bg-[#201D1D] shadow-[0_0_40px_rgba(104,64,255,0.25)]"
                  : "border border-[#312E2E] bg-[#201D1D]/70 hover:border-[#4F4C4C]"
              }`}
              key={tier.name}
            >
              {tier.featured && (
                <div className="absolute -top-3.5 left-1/2 z-10 -translate-x-1/2">
                  <span className="inline-flex items-center gap-1.5 rounded-full bg-[#A1FF62] px-4 py-1 font-hafferMono text-[10px] uppercase font-bold text-[#201D1D] shadow-md">
                    <Zap className="size-3 fill-current" /> Core Workflow
                  </span>
                </div>
              )}

              <div>
                <h3 className="font-hafferVf text-lg font-bold text-[#F4F4F4]">{tier.name}</h3>
                <div className="mt-4 flex items-baseline gap-1">
                  <span className="font-hafferXh text-4xl font-normal text-[#F4F4F4]">{tier.stat}</span>
                </div>
                <p className="mt-3 text-xs leading-5 text-[#817F7F]">
                  {tier.description}
                </p>

                <div className="my-6 border-t border-[#312E2E]" />

                <ul className="space-y-3">
                  {tier.features.map((feature) => (
                    <li className="flex items-start gap-2.5 text-xs text-[#F4F4F4]/90" key={feature}>
                      <div className="mt-0.5 flex size-4 shrink-0 items-center justify-center rounded-full bg-[#6840FF]/20 text-[#6840FF]">
                        <Check className="size-2.5 stroke-[3]" />
                      </div>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mt-8">
                <button
                  className={`w-full text-center text-sm font-medium transition-all duration-200 ${
                    tier.featured
                      ? "btn-osmo-purple py-3"
                      : "btn-osmo-stroke py-3 hover:border-[#817F7F]"
                  }`}
                  type="button"
                >
                  {tier.cta}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
