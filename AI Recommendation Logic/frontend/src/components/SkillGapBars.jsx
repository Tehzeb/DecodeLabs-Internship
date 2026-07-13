import { motion } from "framer-motion";
import { Check, X } from "lucide-react";

export default function SkillGapBars({ career }) {
  const sorted = [...career.skill_breakdown].sort((a, b) => b.importance - a.importance);
  const maxImportance = 5;

  return (
    <div className="rounded-2xl border border-border bg-surface p-5 md:p-6">
      <div className="flex items-center justify-between mb-1">
        <h3 className="font-display font-semibold">Skill-gap breakdown</h3>
        <span className="text-xs font-mono text-dim">for {career.title}</span>
      </div>
      <p className="text-sm text-dim mb-5">
        Importance-weighted coverage: <span className="text-accent font-semibold">{career.skill_coverage_pct}%</span>
      </p>

      <div className="space-y-3">
        {sorted.map((s, i) => (
          <div key={s.skill}>
            <div className="flex items-center justify-between text-sm mb-1">
              <span className="flex items-center gap-1.5 font-medium">
                {s.has_skill ? (
                  <Check size={13} className="text-accent2" />
                ) : (
                  <X size={13} className="text-dim" />
                )}
                {s.skill}
              </span>
              <span className="font-mono text-xs text-dim">importance {s.importance}/5</span>
            </div>
            <div className="h-2 rounded-full bg-surface2 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${(s.importance / maxImportance) * 100}%` }}
                transition={{ duration: 0.7, delay: 0.05 * i, ease: "easeOut" }}
                className={`h-full rounded-full ${s.has_skill ? "bg-accent2" : "bg-border"}`}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
