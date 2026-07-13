import { useState, useMemo } from "react";
import { motion } from "framer-motion";
import CareerCard from "./CareerCard";
import ConstellationViz from "./ConstellationViz";
import SkillGapBars from "./SkillGapBars";
import CourseCard from "./CourseCard";
import SimilarPaths from "./SimilarPaths";

export default function ResultsDashboard({ data }) {
  const [selectedSoc, setSelectedSoc] = useState(data.focus_career.soc);

  const selectedCareer = useMemo(
    () => data.top_careers.find((c) => c.soc === selectedSoc) || data.focus_career,
    [selectedSoc, data]
  );

  return (
    <motion.section
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="max-w-6xl mx-auto px-6 py-16 space-y-10"
    >
      <div>
        <p className="text-xs font-mono uppercase tracking-widest text-accent mb-1">01 — content match</p>
        <h2 className="font-display text-2xl font-semibold mb-5">Your top career matches</h2>
        <div className="grid md:grid-cols-3 gap-4">
          {data.top_careers.map((c, i) => (
            <CareerCard
              key={c.soc}
              career={c}
              index={i}
              active={c.soc === selectedSoc}
              onSelect={() => setSelectedSoc(c.soc)}
            />
          ))}
        </div>
      </div>

      <div>
        <p className="text-xs font-mono uppercase tracking-widest text-accent mb-1">skill constellation</p>
        <h2 className="font-display text-2xl font-semibold mb-2">How your skills connect</h2>
        <p className="text-sm text-dim mb-5 max-w-2xl">
          Solid lines from a career node trace skills you already have; dashed, dimmer nodes are the
          ones still open for <span className="text-text font-medium">{selectedCareer.title}</span>.
        </p>
        <div className="rounded-2xl border border-border bg-surface p-4 md:p-6">
          <ConstellationViz careers={data.top_careers} focusCareer={selectedCareer} />
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6 items-start">
        <div>
          <p className="text-xs font-mono uppercase tracking-widest text-accent mb-1">02 — skill-gap scoring</p>
          <h2 className="font-display text-2xl font-semibold mb-5">Close the gap</h2>
          <SkillGapBars career={selectedCareer} />
        </div>
        <div>
          <p className="text-xs font-mono uppercase tracking-widest text-accent mb-1">context</p>
          <h2 className="font-display text-2xl font-semibold mb-5">About this role</h2>
          <div className="rounded-2xl border border-border bg-surface p-5 md:p-6 space-y-3">
            <p className="text-sm text-dim">{selectedCareer.description}</p>
            <div className="flex flex-wrap gap-2 pt-1">
              {selectedCareer.interests.map((t) => (
                <span key={t} className="text-[11px] px-2.5 py-1 rounded-full bg-surface2 border border-border text-dim">
                  {t}
                </span>
              ))}
            </div>
            <p className="text-xs font-mono text-dim pt-2">
              O*NET-SOC {selectedCareer.soc} · ${selectedCareer.salary_low.toLocaleString()}–${selectedCareer.salary_high.toLocaleString()}/yr
            </p>
          </div>
        </div>
      </div>

      <div>
        <p className="text-xs font-mono uppercase tracking-widest text-accent mb-1">03 — course recommendations</p>
        <h2 className="font-display text-2xl font-semibold mb-5">Courses that close your gap fastest</h2>
        {data.recommended_courses.length === 0 ? (
          <p className="text-sm text-dim">No gap left to close — you already cover every core skill for this role.</p>
        ) : (
          <div className="grid md:grid-cols-3 gap-4">
            {data.recommended_courses.map((c, i) => (
              <CourseCard key={c.course_id} course={c} index={i} />
            ))}
          </div>
        )}
      </div>

      <SimilarPaths paths={data.similar_learner_paths} />

      <p className="text-center text-[11px] font-mono text-dim pt-4">
        computed {new Date(data.generated_at).toLocaleString()} · {data.method_notes.career_matching}
      </p>
    </motion.section>
  );
}
