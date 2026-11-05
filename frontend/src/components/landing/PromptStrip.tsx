import { useState } from "react";
import { ArrowRight, Zap } from "lucide-react";

const prompts = [
  { label: "Calculate $50,000 loan EMI with 8.5% interest", desk: "Finance", color: "text-[#A1FF62]", bg: "bg-[#A1FF62]/10", hint: "Executes calculate_emi tool" },
  { label: "Build 5-day budget itinerary for Tokyo", desk: "Travel", color: "text-[#6840FF]", bg: "bg-[#6840FF]/15", hint: "Executes estimate_trip_budget & transport" },
  { label: "Draft sprint kickoff & retrospective meeting agenda", desk: "Planning", color: "text-[#F84131]", bg: "bg-[#F84131]/10", hint: "Executes generate_meeting_agenda" },
  { label: "Scale chicken alfredo recipe to 8 servings with shopping list", desk: "Kitchen", color: "text-[#A1FF62]", bg: "bg-[#A1FF62]/10", hint: "Executes scale_recipe & shopping_list" },
  { label: "Create 4-block Pomodoro exam revision plan", desk: "Study", color: "text-[#6840FF]", bg: "bg-[#6840FF]/15", hint: "Executes pomodoro_plan & flashcards" },
  { label: "Software Engineer resume checklist & outreach draft", desk: "Career", color: "text-[#F84131]", bg: "bg-[#F84131]/10", hint: "Executes resume_checklist & skill_gap" },
  { label: "Check 5-day weather conditions & clothing advice for London", desk: "Weather", color: "text-[#A1FF62]", bg: "bg-[#A1FF62]/10", hint: "Executes get_current_weather & forecast" },
  { label: "Calculate BMI, calorie targets & 4-day workout split", desk: "Health", color: "text-[#6840FF]", bg: "bg-[#6840FF]/15", hint: "Executes bmi_report & workout_split" },
];

export function PromptStrip() {
  const [active, setActive] = useState<number | null>(null);

  return (
    <section className="border-y border-[#312E2E] bg-[#151313] px-4 py-12 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-6xl">
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="flex size-6 items-center justify-center rounded-full bg-[#6840FF]/20 text-[#6840FF]">
              <Zap className="size-3.5 fill-current" />
            </div>
            <span className="font-hafferXh text-sm font-normal text-[#F4F4F4]">
              Interactive Multi-Agent Playground
            </span>
            <span className="hidden text-xs text-[#817F7F] sm:inline">
              — Click any prompt to see which specialist desk handles it
            </span>
          </div>
          <span className="font-hafferMono text-[10px] uppercase text-[#A1FF62]">
            8 Desks Connected
          </span>
        </div>

        {/* Prompt Chips */}
        <div className="flex flex-wrap gap-2.5">
          {prompts.map((prompt, i) => {
            const isSelected = active === i;
            return (
              <button
                className={`group flex items-center gap-2.5 rounded-full border px-4 py-2 text-xs transition-all duration-200 ${
                  isSelected
                    ? "border-[#A1FF62] bg-[#201D1D] text-[#F4F4F4] shadow-[0_0_20px_rgba(161,255,98,0.2)]"
                    : "border-[#312E2E] bg-[#201D1D] text-[#B8B8B8] hover:border-[#817F7F] hover:text-[#F4F4F4]"
                }`}
                key={prompt.label}
                onClick={() => setActive(isSelected ? null : i)}
                type="button"
              >
                <span>{prompt.label}</span>
                <span className={`rounded-full px-2 py-0.5 text-[10px] ${prompt.bg} ${prompt.color} font-hafferMono uppercase`}>
                  {prompt.desk} Desk
                </span>
                <ArrowRight className="size-3 opacity-0 transition-opacity duration-200 group-hover:opacity-100" />
              </button>
            );
          })}
        </div>

        {/* Simulated routing banner */}
        {active !== null && (
          <div className="mt-5 animate-osmo-up rounded-xl border border-[#312E2E] bg-[#201D1D] p-4 shadow-xl">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-2.5">
                <span className="size-2 rounded-full bg-[#A1FF62] animate-ping" />
                <span className="text-xs text-[#817F7F]">Routed to Desk:</span>
                <span className={`rounded-full px-2.5 py-0.5 text-xs font-hafferMono uppercase ${prompts[active].bg} ${prompts[active].color}`}>
                  {prompts[active].desk} Desk
                </span>
                <span className="text-xs text-[#B8B8B8]">({prompts[active].hint})</span>
              </div>
              <span className="font-hafferMono text-[11px] text-[#A1FF62]">
                ✓ Validated & Ready
              </span>
            </div>
            <p className="mt-2 text-xs text-[#F4F4F4]/80">
              Query: &quot;{prompts[active].label}&quot;
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
