import { Navbar } from "@/components/landing/Navbar";
import { Hero } from "@/components/landing/Hero";
import { PromptStrip } from "@/components/landing/PromptStrip";
import { BentoGrid } from "@/components/landing/BentoGrid";
import { Architecture } from "@/components/landing/Architecture";
import { PricingTable } from "@/components/landing/PricingTable";
import { CtaBanner, Footer } from "@/components/landing/Footer";

interface LandingPageProps {
  onLaunchApp: () => void;
}

export function LandingPage({ onLaunchApp }: LandingPageProps) {
  return (
    <div className="landing-bg min-h-screen">
      <Navbar onLaunchApp={onLaunchApp} />
      <Hero onLaunchApp={onLaunchApp} />
      <PromptStrip />
      <BentoGrid />
      <Architecture />
      <PricingTable />
      <CtaBanner onLaunchApp={onLaunchApp} />
      <Footer />
    </div>
  );
}

export default LandingPage;
