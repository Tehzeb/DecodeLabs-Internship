import { motion } from "framer-motion";
import { Compass } from "lucide-react";

export default function Loader() {
  return (
    <div className="flex flex-col items-center justify-center py-16 gap-5">
      <div className="relative w-24 h-24">
        <motion.div
          className="absolute inset-0 rounded-full border border-dashed border-accent/40"
          animate={{ rotate: 360 }}
          transition={{ duration: 6, repeat: Infinity, ease: "linear" }}
        />
        <motion.div
          className="absolute inset-3 rounded-full border border-dashed border-accent2/40"
          animate={{ rotate: -360 }}
          transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
        />
        <div className="absolute inset-0 flex items-center justify-center">
          <Compass size={28} className="text-accent animate-pulse" />
        </div>
      </div>
      <p className="text-sm font-mono text-dim">running TF-IDF · cosine similarity · skill-gap scoring…</p>
    </div>
  );
}
