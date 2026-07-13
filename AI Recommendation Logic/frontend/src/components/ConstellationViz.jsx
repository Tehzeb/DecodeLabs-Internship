import { useMemo } from "react";
import { motion } from "framer-motion";

const WIDTH = 820;
const HEIGHT = 460;
const CENTER = { x: WIDTH / 2, y: HEIGHT / 2 + 10 };

function polar(cx, cy, r, angleDeg) {
  const rad = (angleDeg * Math.PI) / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}

export default function ConstellationViz({ careers, focusCareer }) {
  const careerNodes = useMemo(() => {
    const n = careers.length;
    const spread = 150; // degrees of arc the careers occupy, centered upward
    const start = -90 - spread / 2;
    return careers.map((c, i) => {
      const angle = n === 1 ? -90 : start + (spread * i) / (n - 1);
      const pos = polar(CENTER.x, CENTER.y, 175, angle);
      return { ...c, ...pos, angle };
    });
  }, [careers]);

  const gapNodes = useMemo(() => {
    if (!focusCareer) return [];
    const focus = careerNodes.find((c) => c.soc === focusCareer.soc) || careerNodes[0];
    if (!focus) return [];
    const skills = [
      ...focusCareer.matched_skills.slice(0, 4).map((s) => ({ skill: s, has: true })),
      ...focusCareer.missing_skills.slice(0, 4).map((s) => ({ skill: s, has: false })),
    ];
    const baseAngle = focus.angle;
    const n = skills.length;
    return skills.map((s, i) => {
      const angle = baseAngle - 55 + (110 * i) / Math.max(n - 1, 1);
      const pos = polar(focus.x, focus.y, 92, angle);
      return { ...s, ...pos, parent: focus };
    });
  }, [focusCareer, careerNodes]);

  return (
    <div className="w-full overflow-x-auto">
      <svg viewBox={`0 0 ${WIDTH} ${HEIGHT}`} className="w-full min-w-[560px] h-auto select-none">
        <defs>
          <radialGradient id="youGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.35" />
            <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
          </radialGradient>
        </defs>

        {/* connecting lines: user -> career */}
        {careerNodes.map((c, i) => (
          <motion.line
            key={`line-${c.soc}`}
            x1={CENTER.x} y1={CENTER.y} x2={c.x} y2={c.y}
            stroke="var(--accent)"
            strokeWidth={1 + (c.match_score / 100) * 3}
            strokeOpacity={0.25 + (c.match_score / 100) * 0.55}
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 1, delay: 0.15 * i, ease: "easeOut" }}
          />
        ))}

        {/* connecting lines: focus career -> skill gap nodes */}
        {gapNodes.map((g, i) => (
          <motion.line
            key={`gap-line-${g.skill}`}
            x1={g.parent.x} y1={g.parent.y} x2={g.x} y2={g.y}
            stroke={g.has ? "var(--accent-2)" : "var(--text-dim)"}
            strokeWidth={1.4}
            strokeDasharray={g.has ? "0" : "3 4"}
            strokeOpacity={g.has ? 0.7 : 0.45}
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 0.8, delay: 0.8 + 0.08 * i, ease: "easeOut" }}
          />
        ))}

        {/* user node */}
        <circle cx={CENTER.x} cy={CENTER.y} r="46" fill="url(#youGlow)" />
        <motion.circle
          cx={CENTER.x} cy={CENTER.y} r="22"
          fill="var(--surface)" stroke="var(--accent)" strokeWidth="2.5"
          initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: "spring", stiffness: 200 }}
        />
        <text x={CENTER.x} y={CENTER.y + 4} textAnchor="middle" className="fill-[color:var(--text)]" fontSize="11" fontFamily="'JetBrains Mono', monospace" fontWeight="600">
          YOU
        </text>

        {/* career nodes */}
        {careerNodes.map((c, i) => (
          <motion.g key={c.soc}
            initial={{ opacity: 0, scale: 0.6 }} animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 + 0.15 * i, type: "spring", stiffness: 220 }}
          >
            <circle cx={c.x} cy={c.y} r={16 + (c.match_score / 100) * 14}
              fill={c.soc === focusCareer?.soc ? "var(--accent)" : "var(--surface2)"}
              stroke="var(--accent)" strokeWidth={c.soc === focusCareer?.soc ? 0 : 1.6} />
            <text x={c.x} y={c.y - (22 + (c.match_score / 100) * 14)} textAnchor="middle"
              fontSize="12.5" fontWeight="600" className="fill-[color:var(--text)]" fontFamily="'Space Grotesk', sans-serif">
              {c.title}
            </text>
            <text x={c.x} y={c.y + 4} textAnchor="middle" fontSize="10.5" fontFamily="'JetBrains Mono', monospace"
              fill={c.soc === focusCareer?.soc ? "#161000" : "var(--accent)"} fontWeight="700">
              {c.match_score}%
            </text>
          </motion.g>
        ))}

        {/* skill gap nodes for focus career */}
        {gapNodes.map((g, i) => (
          <motion.g key={g.skill}
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 1 + 0.08 * i }}
          >
            <circle cx={g.x} cy={g.y} r="4.5"
              fill={g.has ? "var(--accent-2)" : "transparent"}
              stroke={g.has ? "var(--accent-2)" : "var(--text-dim)"} strokeWidth="1.4" />
            <text x={g.x} y={g.y - 10} textAnchor="middle" fontSize="9.5"
              fontFamily="'JetBrains Mono', monospace"
              fill={g.has ? "var(--accent-2)" : "var(--text-dim)"}>
              {g.skill.length > 16 ? g.skill.slice(0, 15) + "…" : g.skill}
            </text>
          </motion.g>
        ))}
      </svg>
    </div>
  );
}
