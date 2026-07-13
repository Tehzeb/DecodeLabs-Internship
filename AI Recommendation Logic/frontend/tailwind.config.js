/** @type {import('tailwindcss').Config} */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        bg: "var(--bg)",
        surface: "var(--surface)",
        surface2: "var(--surface-2)",
        border: "var(--border)",
        text: "var(--text)",
        dim: "var(--text-dim)",
        accent: "var(--accent)",
        accent2: "var(--accent-2)",
        danger: "var(--danger)",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      boxShadow: {
        glow: "0 0 0 1px var(--border), 0 8px 30px -8px rgba(242, 184, 75, 0.25)",
        card: "0 1px 2px rgba(0,0,0,0.04), 0 8px 24px -12px rgba(0,0,0,0.18)",
      },
      keyframes: {
        drift: {
          "0%, 100%": { transform: "translate(0,0)" },
          "50%": { transform: "translate(12px,-10px)" },
        },
        pulseRing: {
          "0%": { opacity: 0.6, transform: "scale(0.95)" },
          "70%": { opacity: 0, transform: "scale(1.4)" },
          "100%": { opacity: 0, transform: "scale(1.4)" },
        },
      },
      animation: {
        drift: "drift 9s ease-in-out infinite",
        pulseRing: "pulseRing 2.4s ease-out infinite",
      },
    },
  },
  plugins: [],
};
