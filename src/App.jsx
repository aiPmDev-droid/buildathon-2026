import { useEffect, useState } from "react"
import { getPerson, runRound } from "./api"
import LandingPage from "./components/LandingPage"
import PhoneFrame from "./components/PhoneFrame"
import SignupScreen from "./components/SignupScreen"
import RoundScreen from "./components/RoundScreen"
import MatchScreen from "./components/MatchScreen"

const STORAGE_KEY = "andermeet_email"

export default function App() {
  const [view, setView] = useState("landing") // landing | app
  const [tab, setTab] = useState("profile")
  const [profile, setProfile] = useState(null)
  const [matchRefreshKey, setMatchRefreshKey] = useState(0)

  useEffect(() => {
    const savedEmail = localStorage.getItem(STORAGE_KEY)
    if (!savedEmail) return
    getPerson(savedEmail)
      .then((p) => {
        setProfile(p)
        setView("app")
      })
      .catch(() => localStorage.removeItem(STORAGE_KEY))
  }, [])

  const handleSignedUp = (saved) => {
    setProfile(saved)
    localStorage.setItem(STORAGE_KEY, saved.email)
  }

  const handleJoinedRound = async (saved) => {
    setProfile(saved)
    localStorage.setItem(STORAGE_KEY, saved.email)
    setView("app")
    try {
      await runRound()
    } catch {
      // fall through — Match tab shows whatever state actually exists
    }
    setMatchRefreshKey((n) => n + 1)
    setTab("match")
  }

  const handleRoundComplete = () => {
    setMatchRefreshKey((n) => n + 1)
    setTab("match")
  }

  if (view === "landing") {
    return <LandingPage onJoin={() => setView("app")} />
  }

  return (
    <PhoneFrame active={tab} onChange={setTab}>
      {tab === "profile" && (
        <SignupScreen
          profile={profile}
          onSignedUp={handleSignedUp}
          onJoinedRound={handleJoinedRound}
        />
      )}
      {tab === "round" && (
        <RoundScreen
          profile={profile}
          onProfileUpdate={setProfile}
          onRoundComplete={handleRoundComplete}
        />
      )}
      {tab === "match" && <MatchScreen profile={profile} refreshKey={matchRefreshKey} />}
    </PhoneFrame>
  )
}
