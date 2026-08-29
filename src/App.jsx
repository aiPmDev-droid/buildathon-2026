import { useEffect, useState } from 'react'

export default function App() {
  const [status, setStatus] = useState('checking')

  useEffect(() => {
    fetch('/api/health')
      .then((res) => res.json())
      .then((data) => setStatus(data.status === 'ok' ? 'ok' : 'error'))
      .catch(() => setStatus('error'))
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-b from-amber-50 to-orange-100 flex items-center justify-center p-6">
      <div className="bg-white rounded-3xl shadow-xl shadow-orange-900/10 p-8 max-w-sm w-full text-center">
        <div className="text-4xl mb-3">☕️</div>
        <h1 className="text-2xl font-semibold text-stone-800 tracking-tight">
          Coffee Roulette
        </h1>
        <p className="text-stone-500 mt-2 text-sm">
          UCLA Anderson coffee chat matching
        </p>
        <div className="mt-6 inline-flex items-center gap-2 rounded-full bg-stone-100 px-4 py-2 text-sm">
          <span
            className={`h-2 w-2 rounded-full ${
              status === 'ok'
                ? 'bg-green-500'
                : status === 'checking'
                  ? 'bg-amber-400 animate-pulse'
                  : 'bg-red-500'
            }`}
          />
          <span className="text-stone-600">
            API: {status === 'checking' ? 'checking…' : status}
          </span>
        </div>
      </div>
    </div>
  )
}
