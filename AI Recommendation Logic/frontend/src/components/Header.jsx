import { motion } from "framer-motion";
import { Compass, Moon, Sun } from "lucide-react";
import { useTheme } from "../context/ThemeContext";

export default function Header() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-40 backdrop-blur-md bg-bg/70 border-b border-border">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <motion.div
            whileHover={{ rotate: 12 }}
            transition={{ type: "spring", stiffness: 300 }}
            className="w-9 h-9 rounded-full bg-accent/15 border border-accent/40 flex items-center justify-center"
          >
            <Compass size={18} className="text-accent" strokeWidth={2.2} />
          </motion.div>
          <div className="leading-tight">
            <p className="font-display font-semibold tracking-tight text-[17px]">VANTAGE</p>
            <p className="text-[11px] font-mono text-dim -mt-0.5">career &amp; skill pathfinder</p>
          </div>
        </div>

        <button
          onClick={toggleTheme}
          aria-label="Toggle color theme"
          className="relative w-11 h-11 rounded-full border border-border bg-surface hover:border-accent/60 transition-colors flex items-center justify-center group"
        >
          <motion.div
            key={theme}
            initial={{ rotate: -90, opacity: 0 }}
            animate={{ rotate: 0, opacity: 1 }}
            transition={{ duration: 0.35 }}
          >
            {theme === "dark" ? (
              <Sun size={17} className="text-accent" />
            ) : (
              <Moon size={17} className="text-accent" />
            )}
          </motion.div>
        </button>
      </div>
    </header>
  );
}
