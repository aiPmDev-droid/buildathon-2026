import { useEffect, useState } from "react"
import { getPerson } from "./api"
import BottomTabBar from "./components/BottomTabBar"
import PhoneFrame from "./components/PhoneFrame"
import SignupScreen from "./components/SignupScreen"
import RoundScreen from "./components/RoundScreen"
import MatchScreen from "./components/MatchScreen"

const STORAGE_KEY = "coffee_roulette_email"

export default function App() {
  const [tab, setTab] = useState("profile")
  const [profile, setProfile] = useState(null)
  const [matchRefreshKey, setMatchRefreshKey] = useState(0)

  useEffect(() => {
    const savedEmail = localStorage.getItem(STORAGE_KEY)
    if (!savedEmail) return
    getPerson(savedEmail)
      .then(setProfile)
      .catch(() => localStorage.removeItem(STORAGE_KEY))
  }, [])

  const handleSignedUp = (saved) => {
    setProfile(saved)
    localStorage.setItem(STORAGE_KEY, saved.email)
  }

  const handleRoundComplete = () => {
    setMatchRefreshKey((n) => n + 1)
    setTab("match")
  }

  return (
    <PhoneFrame>
      {tab === "profile" && <SignupScreen profile={profile} onSignedUp={handleSignedUp} />}
      {tab === "round" && (
        <RoundScreen
          profile={profile}
          onProfileUpdate={setProfile}
          onRoundComplete={handleRoundComplete}
        />
      )}
      {tab === "match" && <MatchScreen profile={profile} refreshKey={matchRefreshKey} />}
      <BottomTabBar active={tab} onChange={setTab} />
    </PhoneFrame>
  )
}
