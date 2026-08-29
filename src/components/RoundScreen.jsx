import { useState } from "react"
import { setOptIn, runRound } from "../api"
import { Screen, Card, Button, Toggle, Toast } from "./ui"

export default function RoundScreen({ profile, onProfileUpdate, onRoundComplete }) {
  const [optInLoading, setOptInLoading] = useState(false)
  const [runLoading, setRunLoading] = useState(false)
  const [toast, setToast] = useState(null)

  if (!profile) {
    return (
      <Screen title="This round" subtitle="Get set up first">
        <Card>
          <p className="text-coffee-600 text-sm leading-relaxed">
            Head to the <span className="font-semibold text-coffee-800">Profile</span> tab and
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
      onProfileUpdate({ ...profile, opted_in: false })
      onRoundComplete(result)
    } catch (err) {
      setToast({ message: err.message, tone: "error" })
    } finally {
      setRunLoading(false)
    }
  }

  return (
    <Screen title="This round" subtitle="Opt in, then run the matching round">
      <Toast {...toast} />
      <Card className="mb-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="font-semibold text-coffee-800">Opt in to this round</p>
            <p className="text-sm text-coffee-500 mt-0.5">
              {profile.opted_in ? "You're in — waiting for the round." : "Not opted in yet."}
            </p>
          </div>
          <Toggle checked={profile.opted_in} onChange={handleToggle} disabled={optInLoading} />
        </div>
      </Card>

      <Card>
        <p className="font-semibold text-coffee-800 mb-1">Run matching round</p>
        <p className="text-sm text-coffee-500 mb-4 leading-relaxed">
          Pairs up everyone currently opted in, skipping repeat matches and people who likely
          already know each other.
        </p>
        <Button onClick={handleRun} loading={runLoading}>
          {runLoading ? "Finding your match…" : "Run matching round"}
        </Button>
      </Card>
    </Screen>
  )
}
