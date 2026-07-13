import { motion } from "framer-motion";
import { Star, Clock, ExternalLink, Users } from "lucide-react";

export default function CourseCard({ course, index }) {
  return (
    <motion.a
      href={course.url}
      target="_blank"
      rel="noopener noreferrer"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.06 * index, duration: 0.45 }}
      whileHover={{ y: -3, borderColor: "var(--accent)" }}
      className="group block rounded-2xl border border-border bg-surface p-5 transition-colors"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-[10px] font-mono uppercase tracking-widest text-dim">{course.provider}</p>
          <h4 className="font-display font-semibold text-[15px] leading-snug mt-1">{course.title}</h4>
        </div>
        <ExternalLink size={15} className="text-dim group-hover:text-accent transition-colors shrink-0 mt-1" />
      </div>

      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 mt-3 text-xs text-dim font-mono">
        <span className="flex items-center gap-1"><Star size={12} className="text-accent" /> {course.rating}</span>
        <span className="flex items-center gap-1"><Clock size={12} /> {course.duration_weeks}w</span>
        <span className="flex items-center gap-1"><Users size={12} /> {course.enrolled_k}k</span>
        <span className="px-1.5 py-0.5 rounded-full bg-surface2">{course.level}</span>
      </div>

      {course.covers_missing_skills?.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mt-3">
          {course.covers_missing_skills.map((s) => (
            <span key={s} className="text-[11px] px-2 py-0.5 rounded-full bg-accent2/10 text-accent2 border border-accent2/30">
              closes: {s}
            </span>
          ))}
        </div>
      )}

      <div className="mt-3 h-1.5 rounded-full bg-surface2 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${course.relevance_score}%` }}
          transition={{ duration: 0.7, delay: 0.06 * index }}
          className="h-full bg-accent rounded-full"
        />
      </div>
      <p className="text-[11px] text-dim mt-1 font-mono">{course.relevance_score}% match to your skill gap</p>
    </motion.a>
  );
}
