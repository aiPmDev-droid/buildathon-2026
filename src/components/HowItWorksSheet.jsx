import { AnimatePresence, motion } from "framer-motion"

const STEPS = [
  {
    icon: "👋",
    title: "Sign up",
    body: "Tell us a bit about yourself: your program, your section, and a couple of quick questions.",
  },
  {
    icon: "🔀",
    title: "Get matched",
    body: "Matching runs the moment you opt in — paired with someone from the Anderson community you probably haven't met, capped at one match per week.",
  },
  {
    icon: "☕",
    title: "Grab coffee",
    body: "You'll get an icebreaker and a way to text each other right in the app to find a time.",
  },
]

function Sheet({ onClose }) {
  return (
    <motion.div
      className="absolute inset-0 z-50 flex items-end bg-navy-900/40"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
    >
      <motion.div
        className="w-full max-h-[85%] overflow-y-auto rounded-t-3xl bg-cream-100 p-5 pb-8"
        initial={{ y: "100%" }}
        animate={{ y: 0 }}
        exit={{ y: "100%" }}
        transition={{ type: "spring", stiffness: 300, damping: 32 }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-1">
          <h2 className="text-xl font-bold text-navy-900">How it works</h2>
          <button
            onClick={onClose}
            aria-label="Close"
            className="h-8 w-8 rounded-full bg-navy-50 flex items-center justify-center text-navy-500"
          >
            ✕
          </button>
        </div>
        <p className="text-sm text-navy-500 mb-5">
          Three simple steps to building deeper connections at Anderson:
        </p>

        <div className="flex flex-col gap-4">
          {STEPS.map((step, i) => (
            <div
              key={step.title}
              className="rounded-2xl bg-white border border-navy-100/70 p-5 text-left shadow-sm"
            >
              <div className="h-10 w-10 rounded-full bg-navy-50 flex items-center justify-center text-lg mb-3">
                {step.icon}
              </div>
              <p className="text-xs font-semibold text-navy-300 mb-1">0{i + 1}</p>
              <p className="font-semibold text-navy-900 mb-1.5">{step.title}</p>
              <p className="text-sm text-navy-500 leading-relaxed">{step.body}</p>
            </div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  )
}

export default function HowItWorksSheet({ open, onClose }) {
  return <AnimatePresence>{open && <Sheet onClose={onClose} />}</AnimatePresence>
}
