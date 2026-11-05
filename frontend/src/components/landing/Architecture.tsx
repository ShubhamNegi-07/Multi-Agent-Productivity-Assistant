import { Cpu, Database, Route, ShieldCheck } from "lucide-react";

const steps = [
  {
    step: "01",
    title: "Domain Prompt Routing",
    description:
      "When you send a message, OmniDesk detects your intent and selects the optimal specialist (Finance, Travel, Health, etc.) with dedicated context.",
    icon: Route,
    badge: "FastAPI Orchestrator",
  },
  {
    step: "02",
    title: "Deterministic Tool Execution",
    description:
      "Numerical calculations, budget splits, weather reports, and checklist structures are executed directly by verified Python tools—eliminating LLM hallucinations.",
    icon: Cpu,
    badge: "Python Tools",
  },
  {
    step: "03",
    title: "Gemini Reasoning & Synthesis",
    description:
      "Google Gemini synthesizes the tool outputs into a clear, grounded, and actionable response, maintaining session history and user preferences.",
    icon: Database,
    badge: "Google Gemini",
  },
  {
    step: "04",
    title: "Structured Output Delivery",
    description:
      "Outputs are formatted with latency metrics, copy actions, and interactive card states for immediate productivity.",
    icon: ShieldCheck,
    badge: "OmniDesk UI",
  },
];

export function Architecture() {
  return (
    <section id="architecture" className="bg-[#151313] px-4 py-20 sm:px-6 lg:px-8 border-t border-[#312E2E]">
      <div className="mx-auto max-w-6xl">
        <div className="mb-14 text-center">
          <div className="osmo-mono-badge mb-3 inline-flex items-center gap-1.5 border border-[#312E2E] bg-[#201D1D] text-[#6840FF]">
            Architecture & Pipeline
          </div>
          <h2 className="font-hafferXh text-3xl font-normal tracking-tight text-[#F4F4F4] sm:text-5xl">
            How OmniDesk Guarantees Precision
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-sm leading-6 text-[#B8B8B8]">
            A decoupled full-stack architecture that marries LLM natural language comprehension
            with the mathematical reliability of Python code.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {steps.map((item) => (
            <div
              className="osmo-card flex flex-col justify-between p-6"
              key={item.step}
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="font-hafferMono text-2xl font-bold text-[#A1FF62]">
                    {item.step}
                  </span>
                  <div className="flex size-9 items-center justify-center rounded-lg bg-[#151313] border border-[#312E2E] text-[#6840FF]">
                    <item.icon className="size-4" />
                  </div>
                </div>

                <div className="mt-4">
                  <span className="font-hafferMono text-[10px] uppercase text-[#817F7F] tracking-wider">
                    {item.badge}
                  </span>
                  <h3 className="mt-1 font-hafferVf text-base font-bold text-[#F4F4F4]">
                    {item.title}
                  </h3>
                  <p className="mt-2 text-xs leading-5 text-[#B8B8B8]">
                    {item.description}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
