const TABS = [
  { id: "profile", label: "Profile", icon: "👤" },
  { id: "round", label: "Round", icon: "☕" },
  { id: "match", label: "Match", icon: "🤝" },
]

export default function BottomTabBar({ active, onChange }) {
  return (
    <nav className="fixed bottom-0 inset-x-0 z-20 pb-[env(safe-area-inset-bottom)]">
      <div className="mx-auto max-w-md bg-white/90 backdrop-blur border-t border-coffee-100 shadow-[0_-4px_20px_-8px_rgba(69,48,31,0.15)]">
        <div className="flex">
          {TABS.map((tab) => {
            const isActive = tab.id === active
            return (
              <button
                key={tab.id}
                onClick={() => onChange(tab.id)}
                className="flex-1 flex flex-col items-center gap-1 py-2.5 transition-colors"
              >
                <span
                  className={`text-xl transition-transform ${isActive ? "scale-110" : "opacity-60"}`}
                >
                  {tab.icon}
                </span>
                <span
                  className={`text-[11px] font-medium transition-colors ${
                    isActive ? "text-terracotta-600" : "text-coffee-300"
                  }`}
                >
                  {tab.label}
                </span>
                <span
                  className={`h-1 w-1 rounded-full transition-opacity ${
                    isActive ? "bg-terracotta-500 opacity-100" : "opacity-0"
                  }`}
                />
              </button>
            )
          })}
        </div>
      </div>
    </nav>
  )
}
