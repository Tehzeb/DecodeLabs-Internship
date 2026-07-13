import { motion } from "framer-motion";
import { Briefcase, DollarSign } from "lucide-react";

function RadialScore({ score, active }) {
  const r = 26;
  const circumference = 2 * Math.PI * r;
  const offset = circumference * (1 - score / 100);
  return (
    <div className="relative w-16 h-16 shrink-0">
      <svg viewBox="0 0 64 64" className="w-16 h-16 -rotate-90">
        <circle cx="32" cy="32" r={r} stroke="var(--border)" strokeWidth="5" fill="none" />
        <motion.circle
          cx="32" cy="32" r={r} stroke={active ? "var(--accent)" : "var(--accent-2)"}
          strokeWidth="5" fill="none" strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: "easeOut" }}
        />
      </svg>
      <div className="absolute inset-0 flex items-center justify-center font-mono text-sm font-bold">
        {score}%
      </div>
    </div>
  );
}

export default function CareerCard({ career, active, onSelect, index }) {
  return (
    <motion.button
      onClick={onSelect}
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.08 * index, duration: 0.5 }}
      whileHover={{ y: -3 }}
      className={`text-left w-full rounded-2xl border p-5 transition-colors ${
        active ? "border-accent bg-accent/[0.07] shadow-glow" : "border-border bg-surface hover:border-accent/40"
      }`}
    >
      <div className="flex items-start gap-4">
        <RadialScore score={career.match_score} active={active} />
        <div className="min-w-0 flex-1">
          <p className="text-[10px] font-mono uppercase tracking-widest text-dim">{career.category}</p>
          <h3 className="font-display font-semibold text-base leading-snug mt-0.5 truncate">{career.title}</h3>
          <p className="text-xs text-dim mt-1.5 flex items-center gap-1.5">
            <DollarSign size={12} />
            ${career.salary_low.toLocaleString()} – ${career.salary_high.toLocaleString()}
          </p>
        </div>
      </div>
      <p className="text-sm text-dim mt-3 line-clamp-2">{career.description}</p>
      <div className="mt-3 flex items-center gap-1.5 text-xs font-mono text-accent2">
        <Briefcase size={12} /> {career.skill_coverage_pct}% skill coverage
      </div>
    </motion.button>
  );
}
