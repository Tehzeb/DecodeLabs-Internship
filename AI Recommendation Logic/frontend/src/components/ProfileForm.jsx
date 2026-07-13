import { motion } from "framer-motion";
import { Sparkles, Loader2 } from "lucide-react";
import ChipInput from "./ChipInput";

export default function ProfileForm({
  skills, setSkills, interests, setInterests, experience, setExperience,
  allSkills, allInterests, onSubmit, loading, error,
}) {
  return (
    <motion.section
      id="console"
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="max-w-4xl mx-auto px-6 -mt-10 relative z-10"
    >
      <div className="rounded-3xl border border-border bg-surface shadow-glow p-6 md:p-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="text-xs font-mono uppercase tracking-widest text-accent">Input console</p>
            <h2 className="font-display text-xl md:text-2xl font-semibold mt-1">Tell us where you stand</h2>
          </div>
          <div className="hidden md:flex items-center gap-1.5 text-dim text-xs font-mono">
            <span className="w-1.5 h-1.5 rounded-full bg-accent2 animate-pulse" />
            live compute — no cached results
          </div>
        </div>

        <div className="grid gap-5">
          <ChipInput
            label="Your skills"
            placeholder="Type a skill and press Enter — e.g. Python, SQL, Linux"
            values={skills}
            onChange={setSkills}
            suggestions={allSkills}
          />

          <ChipInput
            label="Interest areas (optional)"
            placeholder="e.g. cybersecurity, data & analytics"
            values={interests}
            onChange={setInterests}
            suggestions={allInterests}
            accentClass="text-accent2"
          />

          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-mono uppercase tracking-wider text-dim">Years of experience</label>
              <span className="font-mono text-sm text-accent">{experience.toFixed(1)} yrs</span>
            </div>
            <input
              type="range" min="0" max="20" step="0.5" value={experience}
              onChange={(e) => setExperience(parseFloat(e.target.value))}
              className="w-full accent-[color:var(--accent)]"
            />
          </div>
        </div>

        {error && (
          <p className="mt-4 text-sm text-danger font-medium">{error}</p>
        )}

        <div className="mt-7 flex justify-end">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            disabled={loading || skills.length === 0}
            onClick={onSubmit}
            className="relative inline-flex items-center gap-2 rounded-full bg-accent text-[#161000] font-semibold px-6 py-3 disabled:opacity-40 disabled:cursor-not-allowed shadow-[0_8px_24px_-8px_rgba(242,184,75,0.6)]"
          >
            {loading ? (
              <>
                <Loader2 size={17} className="animate-spin" /> Computing…
              </>
            ) : (
              <>
                <Sparkles size={17} /> Compute my recommendations
              </>
            )}
          </motion.button>
        </div>
      </div>
    </motion.section>
  );
}
