import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import AssistantPage from "@/pages/AssistantPage";
import "./styles.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AssistantPage />
  </StrictMode>,
);
