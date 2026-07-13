import { motion } from "framer-motion";
import { Users2, Info } from "lucide-react";

export default function SimilarPaths({ paths }) {
  if (!paths?.length) return null;
  return (
    <div className="rounded-2xl border border-border bg-surface p-5 md:p-6">
      <div className="flex items-center gap-2 mb-1">
        <Users2 size={16} className="text-accent" />
        <h3 className="font-display font-semibold">People on a similar path also explore</h3>
      </div>
      <p className="text-xs text-dim mb-4 flex items-start gap-1.5">
        <Info size={13} className="mt-0.5 shrink-0" />
        Proxy signal — computed from skill-space neighbors in the real occupation dataset, not from
        real user interaction logs (none exist publicly for this task).
      </p>
      <div className="grid sm:grid-cols-3 gap-3">
        {paths.map((p, i) => (
          <motion.div
            key={p.title}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 * i }}
            className="rounded-xl bg-surface2 border border-border p-4"
          >
            <p className="text-[10px] font-mono uppercase tracking-wider text-dim">{p.category}</p>
            <p className="font-medium mt-1">{p.title}</p>
            <p className="text-xs text-dim mt-2">{p.reason}</p>
            <p className="text-[11px] font-mono text-accent2 mt-2">
              {Math.round(p.shared_skill_ratio * 100)}% skill overlap
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
