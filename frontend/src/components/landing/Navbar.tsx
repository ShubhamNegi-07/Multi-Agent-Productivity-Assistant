import { useState } from "react";
import {
  ChevronDown,
  Menu,
  X,
  Zap,
} from "lucide-react";
import { OmniLogo } from "@/components/brand/OmniLogo";

interface NavbarProps {
  onLaunchApp: () => void;
}

const deskLinks = [
  { name: "Weather Desk", id: "weather", desc: "Live conditions & forecasts" },
  { name: "Travel Desk", id: "travel", desc: "Itineraries & trip budgets" },
  { name: "Finance Desk", id: "finance", desc: "EMI, loans & budget splits" },
  { name: "Planning Desk", id: "productivity", desc: "Agendas & structured todos" },
  { name: "Career Desk", id: "career", desc: "Skill gaps & outreach" },
  { name: "Health Desk", id: "health", desc: "Calories, workouts & BMI" },
  { name: "Kitchen Desk", id: "recipe", desc: "Recipe scaling & shopping lists" },
  { name: "Study Desk", id: "study", desc: "Pomodoros & exam schedules" },
];

export function Navbar({ onLaunchApp }: NavbarProps) {
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [isDesksOpen, setIsDesksOpen] = useState(false);

  return (
    <nav className="fixed inset-x-0 top-0 z-50 glass border-b border-[#312E2E] font-hafferXh">
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand Logo */}
        <button className="cursor-pointer" onClick={onLaunchApp} type="button" aria-label="Open OmniDesk">
          <OmniLogo />
        </button>

        {/* Desktop Navigation */}
        <div className="hidden items-center gap-1 md:flex">
          <div className="relative">
            <button
              className="flex items-center gap-1.5 rounded-full px-4 py-2 text-sm text-[#B8B8B8] transition-colors hover:text-[#F4F4F4]"
              onClick={() => setIsDesksOpen(!isDesksOpen)}
              onBlur={() => setTimeout(() => setIsDesksOpen(false), 200)}
              type="button"
            >
              8 Specialist Desks <ChevronDown className="size-3 text-[#817F7F]" />
            </button>
            {isDesksOpen && (
              <div className="absolute left-0 top-full mt-2 w-64 rounded-xl border border-[#312E2E] bg-[#201D1D]/95 p-2 shadow-2xl backdrop-blur-xl animate-osmo-up">
                {deskLinks.map((desk) => (
                  <a
                    className="flex flex-col rounded-lg px-3 py-2 transition-colors hover:bg-[#151313] hover:text-[#A1FF62]"
                    href={`#desks`}
                    key={desk.id}
                  >
                    <div className="flex items-center gap-2">
                      <span className="size-1.5 rounded-full bg-[#A1FF62]" />
                      <span className="font-hafferXh text-xs font-semibold text-[#F4F4F4]">{desk.name}</span>
                    </div>
                    <span className="text-[10px] text-[#817F7F] pl-3.5">{desk.desc}</span>
                  </a>
                ))}
              </div>
            )}
          </div>

          <a
            className="rounded-full px-4 py-2 text-sm text-[#B8B8B8] transition-colors hover:text-[#F4F4F4]"
            href="#architecture"
          >
            How It Works
          </a>
          <a
            className="rounded-full px-4 py-2 text-sm text-[#B8B8B8] transition-colors hover:text-[#F4F4F4]"
            href="#desks"
          >
            Specialists
          </a>
          <a
            className="rounded-full px-4 py-2 text-sm text-[#B8B8B8] transition-colors hover:text-[#F4F4F4]"
            href="#platform"
          >
            About OmniDesk
          </a>
        </div>

        {/* Action Buttons */}
        <div className="hidden items-center gap-3 md:flex">
          <button
            className="btn-osmo-purple text-sm py-2 px-6"
            onClick={onLaunchApp}
            type="button"
          >
            <Zap className="size-3.5 fill-current text-[#A1FF62]" />
            Open OmniDesk
          </button>
        </div>

        {/* Mobile Toggle */}
        <button
          className="inline-flex size-10 items-center justify-center rounded-full text-[#F4F4F4] hover:bg-[#201D1D] md:hidden"
          onClick={() => setIsMobileOpen(!isMobileOpen)}
          type="button"
          aria-label="Toggle menu"
        >
          {isMobileOpen ? <X className="size-5" /> : <Menu className="size-5" />}
        </button>
      </div>

      {/* Mobile Drawer */}
      {isMobileOpen && (
        <div className="border-t border-[#312E2E] bg-[#151313]/95 px-5 pb-8 pt-4 backdrop-blur-2xl md:hidden">
          <div className="space-y-1">
            {deskLinks.map((desk) => (
              <a
                className="block rounded-lg px-3 py-2 text-sm text-[#B8B8B8] transition-colors hover:text-[#A1FF62]"
                href={`#desks`}
                key={desk.id}
                onClick={() => setIsMobileOpen(false)}
              >
                {desk.name}
              </a>
            ))}
          </div>
          <div className="mt-5 flex flex-col gap-2.5 border-t border-[#312E2E] pt-5">
            <button
              className="btn-osmo-purple w-full justify-center"
              onClick={() => { setIsMobileOpen(false); onLaunchApp(); }}
              type="button"
            >
              <Zap className="size-3.5 fill-current text-[#A1FF62]" />
              Enter workspace
            </button>
          </div>
        </div>
      )}
    </nav>
  );
}
