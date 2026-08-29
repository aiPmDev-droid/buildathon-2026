export function Screen({ title, subtitle, children }) {
  return (
    <div className="min-h-full bg-gradient-to-b from-cream-100 to-cream-200 pb-10 pt-10 px-5">
      <div className="mx-auto max-w-md">
        {title && (
          <header className="mb-6 px-1">
            <h1 className="font-serif text-3xl font-semibold text-coffee-900 tracking-tight">
              {title}
            </h1>
            {subtitle && <p className="mt-1 text-sm text-coffee-500">{subtitle}</p>}
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
      className={`bg-white rounded-3xl shadow-lg shadow-coffee-900/5 border border-coffee-100/60 p-6 ${className}`}
    >
      {children}
    </div>
  )
}

export function Field({ label, children }) {
  return (
    <label className="block mb-4">
      <span className="block text-sm font-medium text-coffee-700 mb-1.5">{label}</span>
      {children}
    </label>
  )
}

export function Input(props) {
  return (
    <input
      {...props}
      className="w-full rounded-xl border border-coffee-100 bg-cream-50 px-4 py-3 text-coffee-900 placeholder:text-coffee-300 outline-none transition-all focus:border-terracotta-400 focus:ring-4 focus:ring-terracotta-400/10"
    />
  )
}

export function Button({ children, loading, variant = "primary", className = "", ...props }) {
  const base =
    "w-full rounded-xl px-4 py-3.5 font-semibold transition-all active:scale-[0.98] disabled:opacity-60 disabled:active:scale-100 flex items-center justify-center gap-2"
  const variants = {
    primary:
      "bg-terracotta-500 text-white shadow-md shadow-terracotta-500/25 hover:bg-terracotta-600",
    secondary: "bg-coffee-100 text-coffee-800 hover:bg-coffee-100/70",
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
        checked ? "bg-sage-500" : "bg-coffee-100"
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
    error: "bg-terracotta-600 text-white",
  }
  return (
    <div
      className={`fixed top-4 inset-x-4 z-30 mx-auto max-w-md rounded-xl px-4 py-3 text-sm font-medium shadow-lg ${tones[tone]} animate-[fade-in_0.2s_ease-out]`}
    >
      {message}
    </div>
  )
}
