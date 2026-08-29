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

export default function LandingPage({ onJoin }) {
  return (
    <div className="min-h-dvh bg-cream-100">
      <header className="max-w-5xl mx-auto px-6 py-6 flex items-center gap-2.5">
        <span className="h-8 w-8 rounded-full bg-navy-700 text-white flex items-center justify-center text-sm">
          ☕
        </span>
        <span className="font-semibold text-navy-900 text-lg">AnderMeet</span>
      </header>

      <main className="max-w-3xl mx-auto px-6 pt-10 pb-24 text-center">
        <span className="inline-flex items-center gap-1.5 rounded-full border border-navy-100 bg-white px-4 py-1.5 text-sm text-navy-500">
          ✨ Weekly matches across the Anderson community
        </span>

        <h1 className="mt-6 text-4xl sm:text-5xl font-bold text-navy-900 tracking-tight leading-[1.1]">
          Meet someone new at
          <br />
          Anderson <span className="text-accent-500">every week.</span>
        </h1>

        <p className="mt-6 text-lg text-navy-500 max-w-xl mx-auto leading-relaxed">
          AnderMeet pairs you with someone outside your usual circle — a different program,
          a different section, someone you probably haven't met — for a coffee chat.
        </p>

        <div className="mt-8 flex items-center justify-center gap-3">
          <button
            onClick={onJoin}
            className="rounded-full bg-navy-700 text-white px-6 py-3 font-semibold hover:bg-navy-800 transition-colors shadow-md shadow-navy-900/15"
          >
            Join AnderMeet
          </button>
          <a
            href="#how-it-works"
            className="rounded-full border border-navy-100 bg-white px-6 py-3 font-semibold text-navy-800 hover:bg-navy-50 transition-colors"
          >
            How it works
          </a>
        </div>
      </main>

      <section id="how-it-works" className="max-w-5xl mx-auto px-6 pb-24">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold text-navy-900">How it works</h2>
          <p className="mt-2 text-navy-500">
            Three simple steps to building deeper connections at Anderson:
          </p>
        </div>

        <div className="grid sm:grid-cols-3 gap-5">
          {STEPS.map((step, i) => (
            <div
              key={step.title}
              className="rounded-2xl bg-white border border-navy-100/70 p-6 text-left shadow-sm"
            >
              <div className="h-10 w-10 rounded-full bg-navy-50 flex items-center justify-center text-lg mb-4">
                {step.icon}
              </div>
              <p className="text-xs font-semibold text-navy-300 mb-1">
                0{i + 1}
              </p>
              <p className="font-semibold text-navy-900 mb-1.5">{step.title}</p>
              <p className="text-sm text-navy-500 leading-relaxed">{step.body}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="border-t border-navy-100">
        <div className="max-w-5xl mx-auto px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-2 text-sm text-navy-500">
          <div className="flex items-center gap-2 font-semibold text-navy-800">
            <span className="h-6 w-6 rounded-full bg-navy-700 text-white flex items-center justify-center text-xs">
              ☕
            </span>
            AnderMeet
          </div>
          <p>Built by Anderson students, for the Anderson community.</p>
        </div>
      </footer>
    </div>
  )
}
