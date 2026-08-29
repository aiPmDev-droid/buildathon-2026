import { useState } from "react"
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

function HowItWorksSheet({ onClose }) {
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

export default function LandingPage({ onJoin }) {
  const [showHowItWorks, setShowHowItWorks] = useState(false)

  return (
    <div className="min-h-full bg-cream-100">
      <header className="px-5 py-5 flex items-center gap-2.5">
        <span className="h-8 w-8 rounded-full bg-navy-700 text-white flex items-center justify-center text-sm">
          ☕
        </span>
        <span className="font-semibold text-navy-900 text-lg">AnderMeet</span>
      </header>

      <main className="px-5 pt-4 pb-10 text-center">
        <span className="inline-flex items-center gap-1.5 rounded-full border border-navy-100 bg-white px-3.5 py-1.5 text-xs text-navy-500">
          ✨ Weekly matches across the Anderson community
        </span>

        <h1 className="mt-5 text-3xl font-bold text-navy-900 tracking-tight leading-[1.15]">
          Meet someone new at Anderson <span className="text-accent-500">every week.</span>
        </h1>

        <p className="mt-4 text-navy-500 leading-relaxed">
          AnderMeet pairs you with someone outside your usual circle — a different program,
          a different section, someone you probably haven't met — for a coffee chat.
        </p>

        <div className="mt-6 flex flex-col items-center gap-3">
          <button
            onClick={onJoin}
            className="w-full rounded-full bg-navy-700 text-white px-6 py-3 font-semibold hover:bg-navy-800 transition-colors shadow-md shadow-navy-900/15"
          >
            Get Started
          </button>
          <button
            onClick={() => setShowHowItWorks(true)}
            className="w-full rounded-full border border-navy-100 bg-white px-6 py-3 font-semibold text-navy-800 hover:bg-navy-50 transition-colors"
          >
            How it Works
          </button>
        </div>
      </main>

      <footer className="border-t border-navy-100">
        <div className="px-5 py-6 flex flex-col items-center gap-2 text-sm text-navy-500 text-center">
          <div className="flex items-center gap-2 font-semibold text-navy-800">
            <span className="h-6 w-6 rounded-full bg-navy-700 text-white flex items-center justify-center text-xs">
              ☕
            </span>
            AnderMeet
          </div>
          <p>Built by Anderson students, for the Anderson community.</p>
        </div>
      </footer>

      <AnimatePresence>
        {showHowItWorks && <HowItWorksSheet onClose={() => setShowHowItWorks(false)} />}
      </AnimatePresence>
    </div>
  )
}
