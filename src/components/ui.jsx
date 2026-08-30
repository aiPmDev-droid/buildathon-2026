export function Screen({ title, subtitle, children }) {
  return (
    <div className="min-h-full bg-gradient-to-b from-cream-100/55 to-cream-200/45 pb-10 pt-10 px-5">
      <div className="mx-auto max-w-md">
        {title && (
          <header className="mb-6 px-1">
            <h1 className="text-3xl font-semibold text-navy-900 tracking-tight">
              {title}
            </h1>
            {subtitle && <p className="mt-1 text-sm text-navy-500">{subtitle}</p>}
          </header>
        )}
        {children}
      </div>
    </div>
  )
}

export function Card({ children, className = "" }) {
  return (
    <div
      className={`bg-white rounded-3xl shadow-lg shadow-navy-900/5 border border-navy-100/60 p-6 ${className}`}
    >
      {children}
    </div>
  )
}

export function Field({ label, children }) {
  return (
    <label className="block mb-4">
      <span className="block text-sm font-medium text-navy-700 mb-1.5">{label}</span>
      {children}
    </label>
  )
}

export function Input(props) {
  return (
    <input
      {...props}
      className="w-full rounded-xl border border-navy-100 bg-cream-50 px-4 py-3 text-navy-900 placeholder:text-navy-300 outline-none transition-all focus:border-accent-400 focus:ring-4 focus:ring-accent-400/10"
    />
  )
}

export function Select({ children, ...props }) {
  return (
    <div className="relative">
      <select
        {...props}
        className="w-full appearance-none rounded-xl border border-navy-100 bg-cream-50 px-4 py-3 text-navy-900 outline-none transition-all focus:border-accent-400 focus:ring-4 focus:ring-accent-400/10"
      >
        {children}
      </select>
      <span className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-navy-300">
        ▾
      </span>
    </div>
  )
}

export function Textarea(props) {
  return (
    <textarea
      {...props}
      rows={props.rows || 3}
      className="w-full rounded-xl border border-navy-100 bg-cream-50 px-4 py-3 text-navy-900 placeholder:text-navy-300 outline-none transition-all focus:border-accent-400 focus:ring-4 focus:ring-accent-400/10 resize-none"
    />
  )
}

export function StepIndicator({ steps, current }) {
  return (
    <div className="flex items-center mb-6">
      {steps.map((label, i) => {
        const n = i + 1
        const done = n < current
        const active = n === current
        return (
          <div key={label} className="flex items-center flex-1 last:flex-none">
            <div className="flex flex-col items-center gap-1.5">
              <div
                className={`h-8 w-8 rounded-full flex items-center justify-center text-sm font-semibold shrink-0 ${
                  done
                    ? "bg-navy-700 text-white"
                    : active
                      ? "bg-navy-50 text-navy-700 ring-2 ring-navy-700"
                      : "bg-navy-50 text-navy-300"
                }`}
              >
                {done ? "✓" : n}
              </div>
              <span
                className={`text-[11px] font-medium whitespace-nowrap ${
                  active || done ? "text-navy-800" : "text-navy-300"
                }`}
              >
                {label}
              </span>
            </div>
            {n < steps.length && (
              <div className={`h-px flex-1 mx-2 mb-5 ${done ? "bg-navy-700" : "bg-navy-100"}`} />
            )}
          </div>
        )
      })}
    </div>
  )
}

export function Button({ children, loading, variant = "primary", className = "", ...props }) {
  const base =
    "w-full rounded-xl px-4 py-3.5 font-semibold transition-all active:scale-[0.98] disabled:opacity-60 disabled:active:scale-100 flex items-center justify-center gap-2"
  const variants = {
    primary:
      "bg-accent-500 text-white shadow-md shadow-accent-500/25 hover:bg-accent-600",
    secondary: "bg-navy-100 text-navy-800 hover:bg-navy-100/70",
  }
  return (
    <button {...props} disabled={loading || props.disabled} className={`${base} ${variants[variant]} ${className}`}>
      {loading && <Spinner />}
      {children}
    </button>
  )
}

export function Spinner({ className = "" }) {
  return (
    <svg
      className={`animate-spin h-4 w-4 text-current ${className}`}
      viewBox="0 0 24 24"
      fill="none"
    >
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path
        className="opacity-90"
        fill="currentColor"
        d="M4 12a8 8 0 018-8v3a5 5 0 00-5 5H4z"
      />
    </svg>
  )
}

export function Toggle({ checked, onChange, disabled }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      disabled={disabled}
      onClick={() => onChange(!checked)}
      className={`relative inline-flex h-8 w-14 shrink-0 items-center rounded-full transition-colors disabled:opacity-60 ${
        checked ? "bg-sage-500" : "bg-navy-100"
      }`}
    >
      <span
        className={`inline-block h-6 w-6 transform rounded-full bg-white shadow transition-transform ${
          checked ? "translate-x-7" : "translate-x-1"
        }`}
      />
    </button>
  )
}

export function Toast({ message, tone = "success" }) {
  if (!message) return null
  const tones = {
    success: "bg-sage-500 text-white",
    error: "bg-accent-600 text-white",
  }
  return (
    <div
      className={`absolute top-4 inset-x-4 z-30 mx-auto max-w-md rounded-xl px-4 py-3 text-sm font-medium shadow-lg ${tones[tone]} animate-[fade-in_0.2s_ease-out]`}
    >
      {message}
    </div>
  )
}
