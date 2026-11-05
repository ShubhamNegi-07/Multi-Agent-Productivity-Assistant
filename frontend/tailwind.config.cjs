/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        sidebar: {
          DEFAULT: "hsl(var(--sidebar))",
          foreground: "hsl(var(--sidebar-foreground))",
        },
        // Osmo Design Reference Tokens (from design.md)
        osmo: {
          bg: "#151313",
          dark: "#201D1D",
          border: "#312E2E",
          text: "#F4F4F4",
          muted: "#B8B8B8",
          sub: "#817F7F",
          lime: "#A1FF62",
          purple: "#6840FF",
          coral: "#F84131",
          neutral550: "#393636",
          neutral525: "#4F4C4C",
          neutral300: "#EAEAEA",
        },
      },
      borderRadius: {
        pill: "51.2px",
        osmoCard: "8.53333px",
        osmoSm: "4.26667px",
        osmoLg: "17.0667px",
      },
      fontFamily: {
        hafferXh: ["'Haffer XH'", "Arial", "sans-serif"],
        hafferVf: ["'Haffer XH'", "Arial", "sans-serif"],
        hafferMono: ["'Haffer XH'", "Arial", "sans-serif"],
        sans: ["'Haffer XH'", "Arial", "sans-serif"],
      },
      transitionTimingFunction: {
        osmo: "cubic-bezier(0.625, 0.05, 0, 1)",
      },
    },
  },
  plugins: [],
};
