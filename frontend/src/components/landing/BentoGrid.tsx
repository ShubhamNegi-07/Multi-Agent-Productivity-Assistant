import { useState } from "react";
import {
  BriefcaseBusiness,
  Calculator,
  ChefHat,
  CloudSun,
  Dumbbell,
  GraduationCap,
  Map,
  NotebookPen,
  type LucideIcon,
  CheckCircle2,
  Thermometer,
  TrendingUp,
  Utensils,
  BookOpen,
} from "lucide-react";

interface DeskConfig {
  id: string;
  name: string;
  icon: LucideIcon;
  tagline: string;
  tools: string;
  color: string;
  bgColor: string;
  preview: React.ReactNode;
}

function FinancePreview() {
  const [amount, setAmount] = useState(60000);
  const rate = 8.5;
  const years = 5;
  const monthlyRate = rate / 1200;
  const months = years * 12;
  const emi = (amount * monthlyRate * Math.pow(1 + monthlyRate, months)) / (Math.pow(1 + monthlyRate, months) - 1);

  return (
    <div className="mt-3.5 space-y-2 rounded-lg bg-[#151313] p-3 border border-[#312E2E]">
      <div className="flex items-center justify-between text-[11px]">
        <span className="text-[#817F7F]">Loan: ${(amount / 1000).toFixed(0)}k @ {rate}%</span>
        <span className="font-hafferMono font-bold text-[#A1FF62]">${emi.toFixed(0)}/mo</span>
      </div>
      <input
        type="range"
        min={10000}
        max={200000}
        step={5000}
        value={amount}
        onChange={(e) => setAmount(Number(e.target.value))}
        className="h-1.5 w-full cursor-pointer appearance-none rounded-full bg-[#312E2E] accent-[#A1FF62]"
      />
    </div>
  );
}

function PlanningPreview() {
  const [checked, setChecked] = useState([true, false, false]);
  const tasks = ["Generate quarterly sprint agenda", "Draft executive update email", "Review prioritization backlog"];
  return (
    <div className="mt-3.5 space-y-2 rounded-lg bg-[#151313] p-3 border border-[#312E2E]">
      {tasks.map((task, i) => (
        <button
          key={task}
          className="flex w-full items-center gap-2 text-left text-[11px]"
          onClick={() => setChecked((c) => c.map((v, j) => (j === i ? !v : v)))}
          type="button"
        >
          <CheckCircle2
            className={`size-3.5 shrink-0 ${checked[i] ? "text-[#A1FF62]" : "text-[#4F4C4C]"}`}
          />
          <span className={checked[i] ? "text-[#817F7F] line-through" : "text-[#F4F4F4]"}>
            {task}
          </span>
        </button>
      ))}
    </div>
  );
}

function WeatherPreview() {
  return (
    <div className="mt-3.5 flex items-center gap-2.5 rounded-lg bg-[#151313] p-3 border border-[#312E2E]">
      <div className="flex items-center gap-1.5 rounded-full bg-[#6840FF]/20 px-2.5 py-1">
        <Thermometer className="size-3 text-[#6840FF]" />
        <span className="font-hafferMono text-[11px] font-bold text-[#6840FF]">24°C</span>
      </div>
      <div className="flex items-center gap-1.5 text-[11px] text-[#817F7F]">
        <CloudSun className="size-3.5 text-[#B8B8B8]" />
        <span>Live forecast verified</span>
      </div>
    </div>
  );
}

function TravelPreview() {
  return (
    <div className="mt-3.5 flex flex-wrap gap-1.5 rounded-lg bg-[#151313] p-3 border border-[#312E2E]">
      {["Day 1: Shibuya", "Day 2: Akihabara", "Day 3: Fuji"].map((d) => (
        <span key={d} className="rounded-full bg-[#A1FF62]/10 px-2.5 py-0.5 text-[10px] font-hafferMono text-[#A1FF62]">
          {d}
        </span>
      ))}
    </div>
  );
}

function SimplePreview({ icon: Icon, label, stat, color }: { icon: LucideIcon; label: string; stat: string; color: string }) {
  return (
    <div className="mt-3.5 flex items-center justify-between rounded-lg bg-[#151313] p-3 border border-[#312E2E]">
      <div className="flex items-center gap-2">
        <Icon className="size-3.5" style={{ color }} />
        <span className="text-[11px] text-[#817F7F]">{label}</span>
      </div>
      <span className="font-hafferMono text-[11px] font-bold" style={{ color }}>{stat}</span>
    </div>
  );
}

const desks: DeskConfig[] = [
  {
    id: "weather",
    name: "Weather Desk",
    icon: CloudSun,
    tagline: "Current conditions, 5-day forecasts, and weather-aware packing guides.",
    tools: "get_current_weather · get_weather_forecast",
    color: "#6840FF",
    bgColor: "bg-[#6840FF]/15",
    preview: <WeatherPreview />,
  },
  {
    id: "travel",
    name: "Travel Desk",
    icon: Map,
    tagline: "Day-by-day itineraries, flight options, transport tips, and trip budgeting.",
    tools: "estimate_trip_budget · suggest_transport · travel_checklist",
    color: "#A1FF62",
    bgColor: "bg-[#A1FF62]/15",
    preview: <TravelPreview />,
  },
  {
    id: "finance",
    name: "Finance Desk",
    icon: Calculator,
    tagline: "Exact loan EMI, simple & compound interest, and 50/30/20 monthly budget splits.",
    tools: "calculate_emi · compound_interest · monthly_budget_split",
    color: "#A1FF62",
    bgColor: "bg-[#A1FF62]/15",
    preview: <FinancePreview />,
  },
  {
    id: "productivity",
    name: "Planning Desk",
    icon: NotebookPen,
    tagline: "Agile meeting agendas, structured to-do lists, professional emails, and study roadmaps.",
    tools: "create_todo_list · generate_meeting_agenda · draft_email",
    color: "#B8B8B8",
    bgColor: "bg-[#393636]",
    preview: <PlanningPreview />,
  },
  {
    id: "career",
    name: "Career Desk",
    icon: BriefcaseBusiness,
    tagline: "Targeted skill gap analysis, recruiter outreach messages, and resume checklists.",
    tools: "skill_gap_analysis · draft_outreach · resume_checklist",
    color: "#6840FF",
    bgColor: "bg-[#6840FF]/15",
    preview: <SimplePreview icon={TrendingUp} label="Skill gap audit" stat="3 Key Gaps" color="#6840FF" />,
  },
  {
    id: "health",
    name: "Health Desk",
    icon: Dumbbell,
    tagline: "BMI calculations, personalized daily calorie targets, and balanced workout splits.",
    tools: "bmi_report · calorie_targets · workout_split",
    color: "#A1FF62",
    bgColor: "bg-[#A1FF62]/15",
    preview: <SimplePreview icon={Dumbbell} label="Hypertrophy split" stat="5 Days/Wk" color="#A1FF62" />,
  },
  {
    id: "recipe",
    name: "Kitchen Desk",
    icon: ChefHat,
    tagline: "Portion scaling, kitchen unit conversions, cooking times, and categorized shopping lists.",
    tools: "scale_recipe · convert_kitchen_measure · shopping_list",
    color: "#F84131",
    bgColor: "bg-[#F84131]/15",
    preview: <SimplePreview icon={Utensils} label="Recipe scaled" stat="8 Servings" color="#F84131" />,
  },
  {
    id: "study",
    name: "Study Desk",
    icon: GraduationCap,
    tagline: "Exam revision schedules, Pomodoro interval plans, and note-to-flashcard generation.",
    tools: "grade_needed · pomodoro_plan · flashcards_from_notes",
    color: "#B8B8B8",
    bgColor: "bg-[#393636]",
    preview: <SimplePreview icon={BookOpen} label="Pomodoro blocks" stat="8 Sessions" color="#B8B8B8" />,
  },
];

export function BentoGrid() {
  return (
    <section id="desks" className="bg-[#151313] px-4 py-24 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <div className="mb-14 text-center">
          <div className="osmo-mono-badge mb-3 inline-flex items-center gap-1.5 border border-[#312E2E] bg-[#201D1D] text-[#A1FF62]">
            Domain Specialization Matrix
          </div>
          <h2 className="font-hafferXh text-3xl font-normal tracking-tight text-[#F4F4F4] sm:text-5xl">
            Eight Focused AI Specialists
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-sm leading-6 text-[#B8B8B8]">
            Each desk is equipped with an isolated domain prompt and testable Python tools.
            Gemini handles natural language; Python handles the math and logic.
          </p>
        </div>

        {/* 8-Card Grid */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {desks.map((desk) => (
            <div
              className="osmo-card group relative flex flex-col justify-between p-5"
              key={desk.id}
            >
              <div>
                <div className="flex items-center justify-between">
                  <div className={`flex size-10 items-center justify-center rounded-lg ${desk.bgColor}`}>
                    <desk.icon className="size-5" style={{ color: desk.color }} />
                  </div>
                  <span className="font-hafferMono text-[10px] uppercase text-[#817F7F]">
                    :{desk.id}
                  </span>
                </div>
                <h3 className="mt-4 font-hafferVf text-base font-bold text-[#F4F4F4]">
                  {desk.name}
                </h3>
                <p className="mt-1 text-xs leading-5 text-[#817F7F]">
                  {desk.tagline}
                </p>
                <div className="mt-2 text-[10px] font-hafferMono text-[#B8B8B8]/60">
                  {desk.tools}
                </div>
              </div>

              {desk.preview}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
