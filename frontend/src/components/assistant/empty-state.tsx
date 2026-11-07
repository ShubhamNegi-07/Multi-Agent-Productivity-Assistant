import {
  ArrowUpRight,
  Compass,
  Layers3,
  Sparkle,
  Target,
  Zap,
} from "lucide-react";

import type { Agent } from "@/lib/api";
import { AgentIcon } from "@/components/assistant/agent-icon";

interface EmptyStateProps {
  agent: Agent;
  onPromptSelect: (prompt: string) => void;
}

const deskCopy: Record<string, {
  intro: string;
  prompts: Array<{ label: string; description: string }>;
}> = {
  weather: {
    intro: "Get instant live conditions, 5-day weather forecasts, and clothing packing advice.",
    prompts: [
      { label: "Check today's weather", description: "Get live temperature, conditions, and outdoor advice." },
      { label: "7-day forecast comparison", description: "Spot major precipitation and temperature shifts." },
      { label: "Packing checklist for weather", description: "Create a clothing checklist based on destination forecast." },
    ],
  },
  travel: {
    intro: "Plan comprehensive day-by-day itineraries, estimate budgets, and suggest transit routes.",
    prompts: [
      { label: "Plan a 4-day city break", description: "Build a structured itinerary with sights and transit options." },
      { label: "Estimate trip budget", description: "Calculate costs for hotels, dining, and daily activities." },
      { label: "Packing & prep checklist", description: "Get documents, gear, and transit arrangements organized." },
    ],
  },
  finance: {
    intro: "Run exact loan calculations, compound interest comparisons, and 50/30/20 budget splits.",
    prompts: [
      { label: "Calculate loan EMI", description: "Compute monthly payment, total interest, and amortization." },
      { label: "Compound interest growth", description: "Project investment returns across 5, 10, and 20 years." },
      { label: "50/30/20 budget breakdown", description: "Split your monthly take-home income into needs, wants, and savings." },
    ],
  },
  productivity: {
    intro: "Organize open tasks into action plans, draft agendas, and compose emails.",
    prompts: [
      { label: "Draft meeting agenda", description: "Create a crisp, goal-oriented schedule for a team kickoff." },
      { label: "Prioritize backlog tasks", description: "Group tasks into high-impact urgent vs scheduled buckets." },
      { label: "Compose outreach email", description: "Draft a concise, professional message with clear call-to-actions." },
    ],
  },
  career: {
    intro: "Audit engineering skills, generate recruiter outreach messages, and check resume standards.",
    prompts: [
      { label: "Skill gap analysis", description: "Identify missing proficiencies for your target senior or staff role." },
      { label: "Draft recruiter outreach", description: "Compose an engaging, high-response message to hiring managers." },
      { label: "Review resume checklist", description: "Verify metrics, action verbs, and formatting standards." },
    ],
  },
  health: {
    intro: "Calculate precise body mass index, daily calorie targets, and balanced weekly workout splits.",
    prompts: [
      { label: "Calculate BMI & category", description: "Determine exact BMI score and healthy weight target range." },
      { label: "Daily calorie targets", description: "Calculate maintenance, cutting, or bulking caloric numbers." },
      { label: "Weekly workout split", description: "Create a push/pull/legs or upper/lower routine based on days." },
    ],
  },
  recipe: {
    intro: "Scale ingredients for any party size, convert kitchen measurements, and generate grocery lists.",
    prompts: [
      { label: "Scale recipe portions", description: "Adjust ingredient ratios perfectly from 2 to 6, 8, or 12 guests." },
      { label: "Convert kitchen measures", description: "Convert cups, grams, tablespoons, and fluid ounces accurately." },
      { label: "Generate shopping list", description: "Group required recipe ingredients by supermarket grocery aisles." },
    ],
  },
  study: {
    intro: "Compute target exam grades needed, generate Pomodoro focus blocks, and turn notes into flashcards.",
    prompts: [
      { label: "Grade needed calculator", description: "Compute the minimum score needed on the final exam to secure an A." },
      { label: "Pomodoro study timetable", description: "Build structured 25/5 focus blocks for difficult coursework." },
      { label: "Create flashcards from notes", description: "Generate active-recall question-and-answer pairs from raw notes." },
    ],
  },
};

export function EmptyState({
  agent,
  onPromptSelect,
}: EmptyStateProps) {
  const copy = deskCopy[agent.id] ?? {
    intro: `${agent.tagline} Submit a question or select an action below to execute verified tools.`,
    prompts: [
      { label: "Run primary calculation", description: "Execute the desk's core deterministic toolchain." },
      { label: "Generate structured breakdown", description: "Organize raw inputs into a clean actionable plan." },
      { label: "Quick analysis", description: "Get immediate recommendations based on constraints." },
    ],
  };
  const promptIcons = [Target, Layers3, Compass];

  return (
    <section className="relative -mt-2 mx-auto w-full max-w-5xl px-4 pb-8 pt-2 sm:px-8 lg:pb-10 lg:pt-4">
      <div className="flex flex-col gap-6">
        {/* Desk Header Banner */}
        <div className="flex flex-col justify-between gap-4 rounded-xl border border-[#312E2E] bg-[#201D1D] p-6 sm:flex-row sm:items-center">
          <div>
            <div className="flex items-center gap-2">
              <span className="rounded-full bg-[#A1FF62]/15 px-3 py-1 font-hafferMono text-[11px] font-bold text-[#A1FF62]">
                {agent.name}
              </span>
              <span className="font-hafferMono text-[11px] text-[#817F7F]">Operational Desk</span>
            </div>
            <p className="mt-2 text-sm leading-6 text-[#B8B8B8]">
              {copy.intro}
            </p>
          </div>
          <div className="flex items-center gap-2 rounded-full border border-[#312E2E] bg-[#151313] px-3.5 py-1.5 text-xs text-[#817F7F]">
            <span className="size-2 rounded-full bg-[#A1FF62] animate-pulse" />
            <span className="text-[#F4F4F4]">Deterministic Tools Connected</span>
          </div>
        </div>

        {/* Action Prompts Grid */}
        <div className="grid min-w-0 grid-cols-1 gap-4 md:grid-cols-3">
          {/* Quick Actions Card */}
          <div className="min-w-0 rounded-xl border border-[#312E2E] bg-[#201D1D] p-5 sm:p-6 md:col-span-2">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-hafferVf text-base font-bold text-[#F4F4F4]">Quick Actions & Prompts</p>
                <p className="mt-1 text-xs text-[#817F7F]">Click any card to start drafting.</p>
              </div>
              <div className="flex size-7 items-center justify-center rounded-full bg-[#A1FF62]/15 text-[#A1FF62]">
                <Sparkle className="size-3.5" />
              </div>
            </div>

            <div className="mt-5 grid min-w-0 grid-cols-1 gap-3 sm:grid-cols-3">
              {copy.prompts.map(({ label, description }, index) => {
                const Icon = promptIcons[index];
                return (
                  <button
                    className="group flex min-h-32 flex-col justify-between rounded-lg border border-[#312E2E] bg-[#151313] p-4 text-left transition-all duration-200 hover:border-[#A1FF62] hover:bg-[#201D1D]"
                    key={label}
                    onClick={() => onPromptSelect(`${label}: ${description}`)}
                    type="button"
                  >
                    <Icon className="size-4 text-[#A1FF62]" aria-hidden="true" />
                    <span>
                      <span className="flex items-center gap-1 font-hafferVf text-xs font-bold text-[#F4F4F4]">
                        {label}
                        <ArrowUpRight className="size-3 opacity-0 transition-opacity group-hover:opacity-100 text-[#A1FF62]" />
                      </span>
                      <span className="mt-1 block text-[11px] leading-4 text-[#817F7F]">{description}</span>
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Desk Execution Specs Card */}
          <div className="min-w-0 rounded-xl border border-[#312E2E] bg-[#201D1D] p-5 sm:p-6">
            <p className="font-hafferVf text-base font-bold text-[#F4F4F4]">Desk Execution Specs</p>
            <p className="mt-1 text-xs text-[#817F7F]">Grounded reasoning & deterministic tools.</p>

            <div className="mt-6 space-y-3">
              <div className="flex items-start gap-3 rounded-lg bg-[#151313] p-3 border border-[#312E2E]">
                <div className="flex size-7 items-center justify-center rounded-lg bg-[#A1FF62]/15 text-[#A1FF62]">
                  <AgentIcon agent={agent} className="size-3.5" aria-hidden="true" />
                </div>
                <div>
                  <p className="text-xs font-bold text-[#F4F4F4]">Zero Hallucination</p>
                  <p className="mt-0.5 text-[11px] text-[#817F7F]">
                    Numeric queries run through verified Python algorithms.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3 rounded-lg bg-[#151313] p-3 border border-[#312E2E]">
                <div className="flex size-7 items-center justify-center rounded-lg bg-[#6840FF]/20 text-[#6840FF]">
                  <Zap className="size-3.5" />
                </div>
                <div>
                  <p className="text-xs font-bold text-[#F4F4F4]">Gemini Reasoning</p>
                  <p className="mt-0.5 text-[11px] text-[#817F7F]">
                    Synthesizes multi-step constraints and plans.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
