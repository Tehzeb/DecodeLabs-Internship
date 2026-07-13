import { motion } from "framer-motion";

function Star({ delay, ...pos }) {
  return (
    <motion.circle
      {...pos}
      r={pos.r}
      fill="var(--accent)"
      className="animate-drift"
      style={{ animationDelay: `${delay}s` }}
      opacity={0.55}
    />
  );
}

export default function Hero({ onStart }) {
  return (
    <section className="relative overflow-hidden pt-20 pb-28">
      <svg className="absolute inset-0 w-full h-full opacity-70" preserveAspectRatio="none">
        <Star cx="8%" cy="20%" r="2" delay={0} />
        <Star cx="18%" cy="55%" r="1.4" delay={1.2} />
        <Star cx="32%" cy="15%" r="1.8" delay={2.1} />
        <Star cx="70%" cy="25%" r="2.2" delay={0.6} />
        <Star cx="85%" cy="60%" r="1.5" delay={1.8} />
        <Star cx="60%" cy="75%" r="1.7" delay={2.6} />
        <Star cx="45%" cy="40%" r="1.3" delay={0.9} />
        <line x1="8%" y1="20%" x2="32%" y2="15%" stroke="var(--border)" strokeWidth="1" />
        <line x1="70%" y1="25%" x2="85%" y2="60%" stroke="var(--border)" strokeWidth="1" />
        <line x1="45%" y1="40%" x2="60%" y2="75%" stroke="var(--border)" strokeWidth="1" />
      </svg>

      <div className="relative max-w-4xl mx-auto px-6 text-center">
        <motion.p
          initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}
          className="font-mono text-xs uppercase tracking-[0.25em] text-accent mb-5"
        >
          hybrid AI recommendation engine
        </motion.p>
        <motion.h1
          initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: 0.1 }}
          className="font-display text-4xl md:text-6xl font-semibold tracking-tight leading-[1.05]"
        >
          Plot your next
          <br />
          <span className="text-accent">career move.</span>
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: 0.2 }}
          className="mt-5 text-dim text-base md:text-lg max-w-xl mx-auto"
        >
          Enter your real skills and interests. Get a live, freshly-computed match against
          real tech occupations, a weighted skill-gap breakdown, and the exact courses that close it.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, delay: 0.3 }}
          className="mt-8"
        >
          <button
            onClick={onStart}
            className="inline-flex items-center gap-2 rounded-full border border-accent/50 bg-accent/10 hover:bg-accent/20 transition-colors px-6 py-3 font-medium"
          >
            Start your profile ↓
          </button>
        </motion.div>
      </div>
    </section>
  );
}
