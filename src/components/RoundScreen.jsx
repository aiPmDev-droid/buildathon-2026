import { useState } from "react"
import { setOptIn, runRound, getPerson } from "../api"
import { Screen, Card, Button, Toggle, Toast, Spinner } from "./ui"

export default function RoundScreen({ profile, onProfileUpdate, onRoundComplete }) {
  const [optInLoading, setOptInLoading] = useState(false)
  const [runLoading, setRunLoading] = useState(false)
  const [toast, setToast] = useState(null)

  if (!profile) {
    return (
      <Screen title="This round" subtitle="Get set up first">
        <Card>
          <p className="text-navy-600 text-sm leading-relaxed">
            Head to the <span className="font-semibold text-navy-800">Profile</span> tab and
            sign up before opting in to a matching round.
          </p>
        </Card>
      </Screen>
    )
  }

  const handleToggle = async (next) => {
    setOptInLoading(true)
    setToast(null)
    try {
      const updated = await setOptIn(profile.email, next)
      onProfileUpdate(updated)

      if (next) {
        // Matching runs the instant you opt in — no waiting for a scheduled round.
        const result = await runRound()
        const gotMatched = result.pairs.some(
          (p) => p.person_a_email === profile.email || p.person_b_email === profile.email
        )
        if (gotMatched) {
          onRoundComplete()
          return
        }
        const fresh = await getPerson(profile.email)
        onProfileUpdate(fresh)
        setToast({
          message: fresh.opted_in
            ? "You're in — no one else eligible right now. We'll try again as soon as someone opts in."
            : "Already matched this week — check back once the cooldown passes.",
          tone: "success",
        })
      }
    } catch (err) {
      setToast({ message: err.message, tone: "error" })
    } finally {
      setOptInLoading(false)
    }
  }

  const handleRun = async () => {
    setRunLoading(true)
    setToast(null)
    try {
      const result = await runRound()
      const fresh = await getPerson(profile.email)
      onProfileUpdate(fresh)
      const gotMatched = result.pairs.some(
        (p) => p.person_a_email === profile.email || p.person_b_email === profile.email
      )
      if (gotMatched) {
        onRoundComplete()
      } else {
        setToast({ message: "Round ran — no new match for you this time.", tone: "success" })
      }
    } catch (err) {
      setToast({ message: err.message, tone: "error" })
    } finally {
      setRunLoading(false)
    }
  }

  return (
    <Screen title="This round" subtitle="Opting in matches you immediately">
      <Toast {...toast} />
      <Card className="mb-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="font-semibold text-navy-800">Opt in to this round</p>
            <p className="text-sm text-navy-500 mt-0.5">
              {profile.opted_in ? "You're in — waiting for the round." : "Not opted in yet."}
            </p>
          </div>
          <Toggle checked={profile.opted_in} onChange={handleToggle} disabled={optInLoading} />
        </div>
        {optInLoading && (
          <div className="mt-3 flex items-center gap-2 text-sm text-accent-600">
            <Spinner className="h-4 w-4" />
            Finding your match…
          </div>
        )}
      </Card>

      <Card>
        <p className="font-semibold text-navy-800 mb-1">Try again</p>
        <p className="text-sm text-navy-500 mb-4 leading-relaxed">
          Re-checks for a match right now — useful if you opted in before anyone else was
          around. Capped at one new match per person per week.
        </p>
        <Button onClick={handleRun} loading={runLoading || optInLoading}>
          {runLoading ? "Finding your match…" : "Run matching round"}
        </Button>
      </Card>
    </Screen>
  )
}
