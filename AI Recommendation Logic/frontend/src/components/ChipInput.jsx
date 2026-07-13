import { useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";

export default function ChipInput({ label, placeholder, values, onChange, suggestions = [], accentClass = "text-accent" }) {
  const [query, setQuery] = useState("");
  const [focused, setFocused] = useState(false);

  const filtered = useMemo(() => {
    if (!query.trim()) return suggestions.filter((s) => !values.includes(s)).slice(0, 8);
    return suggestions
      .filter((s) => s.toLowerCase().includes(query.toLowerCase()) && !values.includes(s))
      .slice(0, 8);
  }, [query, suggestions, values]);

  const addValue = (val) => {
    const v = val.trim();
    if (!v) return;
    if (!values.includes(v)) onChange([...values, v]);
    setQuery("");
  };

  const removeValue = (val) => onChange(values.filter((v) => v !== val));

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      if (filtered.length > 0) addValue(filtered[0]);
      else addValue(query);
    } else if (e.key === "Backspace" && !query && values.length) {
      removeValue(values[values.length - 1]);
    }
  };

  return (
    <div>
      {label && <label className="block text-xs font-mono uppercase tracking-wider text-dim mb-2">{label}</label>}
      <div
        className="chip-input flex flex-wrap items-center gap-2 min-h-[52px] px-3 py-2.5 rounded-xl border border-border bg-surface2 focus-within:border-accent/70 transition-colors"
        onClick={() => document.getElementById(`chip-input-${label}`)?.focus()}
      >
        <AnimatePresence initial={false}>
          {values.map((v) => (
            <motion.span
              key={v}
              layout
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              className={`inline-flex items-center gap-1 rounded-full bg-accent/15 border border-accent/40 pl-3 pr-1.5 py-1 text-sm font-medium ${accentClass}`}
            >
              {v}
              <button
                type="button"
                onClick={(e) => { e.stopPropagation(); removeValue(v); }}
                className="rounded-full hover:bg-accent/25 p-0.5"
                aria-label={`Remove ${v}`}
              >
                <X size={12} />
              </button>
            </motion.span>
          ))}
        </AnimatePresence>
        <input
          id={`chip-input-${label}`}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => setFocused(true)}
          onBlur={() => setTimeout(() => setFocused(false), 150)}
          placeholder={values.length === 0 ? placeholder : ""}
          className="flex-1 min-w-[120px] text-sm py-1"
        />
      </div>

      <AnimatePresence>
        {focused && filtered.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -6 }}
            className="relative"
          >
            <div className="absolute z-20 mt-1.5 w-full max-h-52 overflow-auto rounded-xl border border-border bg-surface shadow-card p-1.5">
              {filtered.map((s) => (
                <button
                  type="button"
                  key={s}
                  onMouseDown={(e) => { e.preventDefault(); addValue(s); }}
                  className="w-full text-left px-3 py-2 rounded-lg text-sm hover:bg-surface2 transition-colors"
                >
                  {s}
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
