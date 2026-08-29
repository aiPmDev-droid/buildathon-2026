import { useEffect, useState } from "react"
import { AnimatePresence, motion } from "framer-motion"
import { getMatch } from "../api"
import { Screen, Card, Spinner, Button } from "./ui"

export default function MatchScreen({ profile, refreshKey }) {
  const [state, setState] = useState("idle") // idle | loading | found | empty | error
  const [match, setMatch] = useState(null)
  const [errorMessage, setErrorMessage] = useState("")
  const [manualRefresh, setManualRefresh] = useState(0)

  useEffect(() => {
    if (!profile) return
    let cancelled = false
    setState("loading")
    getMatch(profile.email)
      .then((data) => {
        if (cancelled) return
        setMatch(data)
        setState("found")
      })
      .catch((err) => {
        if (cancelled) return
        if (err.message === "No match yet") {
          setState("empty")
        } else {
          setErrorMessage(err.message)
          setState("error")
        }
      })
    return () => {
      cancelled = true
    }
  }, [profile, refreshKey, manualRefresh])

  if (!profile) {
    return (
      <Screen title="Your match" subtitle="Get set up first">
        <Card>
          <p className="text-coffee-600 text-sm leading-relaxed">
            Sign up on the <span className="font-semibold text-coffee-800">Profile</span> tab to
            see your matches here.
          </p>
        </Card>
      </Screen>
    )
  }

  return (
    <Screen title="Your match" subtitle="Round reveal">
      <AnimatePresence mode="wait">
        {state === "loading" && (
          <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <Card className="flex flex-col items-center gap-3 py-10">
              <Spinner className="h-8 w-8 text-terracotta-500" />
              <p className="text-coffee-500 text-sm">Finding your match…</p>
            </Card>
          </motion.div>
        )}

        {state === "empty" && (
          <motion.div
            key="empty"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <Card className="text-center py-10">
              <div className="text-3xl mb-2">🫙</div>
              <p className="font-semibold text-coffee-800">No match yet</p>
              <p className="text-sm text-coffee-500 mt-1">
                Opt in on the Round tab, then wait for the next matching round to run.
              </p>
            </Card>
          </motion.div>
        )}

        {state === "error" && (
          <motion.div key="error" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <Card className="text-center py-10">
              <p className="text-terracotta-600 font-medium">{errorMessage}</p>
            </Card>
          </motion.div>
        )}

        {state === "found" && match && (
          <motion.div
            key="found"
            initial={{ opacity: 0, scale: 0.92, y: 12 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ type: "spring", stiffness: 260, damping: 22 }}
          >
            <Card>
              <div className="flex items-center gap-4">
                <div className="h-14 w-14 shrink-0 rounded-full bg-gradient-to-br from-terracotta-400 to-terracotta-600 flex items-center justify-center text-white text-xl font-serif font-semibold">
                  {match.partner.name.trim().charAt(0).toUpperCase()}
                </div>
                <div>
                  <p className="text-xs uppercase tracking-wide text-coffee-400 font-medium">
                    Round {match.round_id}
                  </p>
                  <h2 className="font-serif text-xl font-semibold text-coffee-900">
                    {match.partner.name}
                  </h2>
                  <p className="text-sm text-coffee-500">{match.partner.program}</p>
                </div>
              </div>

              <div className="mt-5 rounded-2xl bg-sage-500/10 border border-sage-500/20 px-4 py-3">
                <p className="text-sm font-medium text-sage-500">{match.shared_interest}</p>
              </div>

              <div className="mt-4">
                <p className="text-xs uppercase tracking-wide text-coffee-400 font-medium mb-1.5">
                  Icebreaker
                </p>
                <p className="text-coffee-700 leading-relaxed">{match.icebreaker}</p>
              </div>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {(state === "found" || state === "empty") && (
        <Button
          variant="secondary"
          className="mt-4"
          onClick={() => setManualRefresh((n) => n + 1)}
        >
          Refresh
        </Button>
      )}
    </Screen>
  )
}
