import {
  BriefcaseBusiness,
  Calculator,
  ChefHat,
  CloudSun,
  Dumbbell,
  GraduationCap,
  Map,
  NotebookPen,
  type LucideProps,
} from "lucide-react";

import type { Agent } from "@/lib/api";

const icons = {
  briefcase: BriefcaseBusiness,
  calculator: Calculator,
  chef: ChefHat,
  "cloud-sun": CloudSun,
  dumbbell: Dumbbell,
  graduation: GraduationCap,
  map: Map,
  notebook: NotebookPen,
} as const;

type AgentIconName = keyof typeof icons;

export function AgentIcon({
  agent,
  ...props
}: { agent: Pick<Agent, "icon"> } & LucideProps) {
  const Icon = icons[agent.icon as AgentIconName] ?? NotebookPen;
  return <Icon {...props} />;
}
