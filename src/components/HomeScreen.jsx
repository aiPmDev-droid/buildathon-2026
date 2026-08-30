import { useState } from "react"
import { Screen, Card } from "./ui"
import HowItWorksSheet from "./HowItWorksSheet"

export default function HomeScreen() {
  const [showHowItWorks, setShowHowItWorks] = useState(false)

  return (
    <Screen title="AnderMeet" subtitle="Weekly matches across the Anderson community">
      <Card className="text-center">
        <span className="inline-flex items-center gap-1.5 rounded-full border border-navy-100 bg-cream-50 px-3.5 py-1.5 text-xs text-navy-500">
          ✨ Meet someone new every week
        </span>
        <h1 className="mt-5 text-2xl font-bold text-navy-900 tracking-tight leading-[1.2]">
          Outside your usual circle, <span className="text-accent-500">on purpose.</span>
        </h1>
        <p className="mt-3 text-sm text-navy-500 leading-relaxed">
          AnderMeet pairs you with someone who shares nothing in common with you, a
          different program, a different section, a different town before Anderson.
        </p>
        <button
          onClick={() => setShowHowItWorks(true)}
          className="mt-5 w-full rounded-full border border-navy-100 bg-white px-6 py-3 font-semibold text-navy-800 hover:bg-navy-50 transition-colors"
        >
          How it Works
        </button>
      </Card>

      <HowItWorksSheet open={showHowItWorks} onClose={() => setShowHowItWorks(false)} />
    </Screen>
  )
}
