import { StrictMode, useState, useCallback } from "react";
import { createRoot } from "react-dom/client";

import LandingPage from "@/pages/LandingPage";
import AssistantPage from "@/pages/AssistantPage";
import "./styles.css";

type View = "landing" | "app";

function App() {
  const [view, setView] = useState<View>("landing");

  const handleLaunchApp = useCallback(() => {
    setView("app");
  }, []);

  const handleBackToLanding = useCallback(() => {
    setView("landing");
  }, []);

  if (view === "landing") {
    return <LandingPage onLaunchApp={handleLaunchApp} />;
  }

  return <AssistantPage onBackToLanding={handleBackToLanding} />;
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
