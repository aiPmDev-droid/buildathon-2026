import { useState } from "react"
import { signup, setOptIn } from "../api"
import {
  Screen,
  Card,
  Field,
  Input,
  Select,
  Textarea,
  Button,
  Toast,
  StepIndicator,
} from "./ui"

const PROGRAMS = ["FT MBA", "FEMBA", "EMBA", "PhD", "MSBA", "MFE", "Faculty/Staff"]

const EMPTY = {
  name: "",
  email: "",
  program: PROGRAMS[0],
  country: "",
  section: "",
  favorite_spot_la: "",
  excited_about: "",
  biggest_challenge: "",
}

const STEP_LABELS = ["The basics", "Where you fit", "About you"]

function EditProfileForm({ profile, onSaved }) {
  const [form, setForm] = useState(profile)
  const [loading, setLoading] = useState(false)
  const [toast, setToast] = useState(null)

  const update = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setToast(null)
    try {
      const saved = await signup(form)
      onSaved(saved)
      setToast({ message: "Profile updated", tone: "success" })
    } catch (err) {
      setToast({ message: err.message, tone: "error" })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Screen title="AnderMeet" subtitle="Your profile">
      <Toast {...toast} />
      <Card>
        <form onSubmit={handleSubmit}>
          <Field label="Name">
            <Input required value={form.name} onChange={update("name")} />
          </Field>
          <Field label="Anderson email">
            <Input required type="email" value={form.email} onChange={update("email")} />
          </Field>
          <Field label="Position">
            <Select required value={form.program} onChange={update("program")}>
              {PROGRAMS.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
            </Select>
          </Field>
          <Field label="Section / subdivision">
            <Input required value={form.section} onChange={update("section")} placeholder="A" />
          </Field>
          <Field label="Country">
            <Input required value={form.country} onChange={update("country")} />
          </Field>
          <Field label="Favorite spot in LA">
            <Input
              required
              value={form.favorite_spot_la}
              onChange={update("favorite_spot_la")}
            />
          </Field>
          <Field label="What are you most excited about right now?">
            <Textarea required value={form.excited_about} onChange={update("excited_about")} />
          </Field>
          <Field label="What's your biggest challenge right now?">
            <Textarea
              required
              value={form.biggest_challenge}
              onChange={update("biggest_challenge")}
            />
          </Field>
          <Button type="submit" loading={loading} className="mt-2">
            Save changes
          </Button>
        </form>
      </Card>
    </Screen>
  )
}

function SignupWizard({ onJoined }) {
  const [step, setStep] = useState(1)
  const [form, setForm] = useState(EMPTY)
  const [loading, setLoading] = useState(false)
  const [toast, setToast] = useState(null)

  const update = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }))

  const stepValid = {
    1: form.name.trim() && form.email.trim(),
    2: form.program.trim() && form.section.trim() && form.country.trim(),
    3:
      form.favorite_spot_la.trim() &&
      form.excited_about.trim() &&
      form.biggest_challenge.trim(),
  }[step]

  const handleJoin = async (e) => {
    e.preventDefault()
    setLoading(true)
    setToast(null)
    try {
      const saved = await signup(form)
      const opted = await setOptIn(saved.email, true)
      onJoined(opted)
    } catch (err) {
      setToast({ message: err.message, tone: "error" })
      setLoading(false)
    }
  }

  return (
    <Screen
      title="Let's get you ready"
      subtitle="Takes about 2 minutes — you can update your answers anytime."
    >
      <Toast {...toast} />
      <Card>
        <StepIndicator steps={STEP_LABELS} current={step} />

        {step === 1 && (
          <div>
            <p className="font-semibold text-navy-900 mb-4">The basics</p>
            <Field label="Name">
              <Input
                autoFocus
                value={form.name}
                onChange={update("name")}
                placeholder="Your name"
              />
            </Field>
            <Field label="Anderson email">
              <Input
                type="email"
                value={form.email}
                onChange={update("email")}
                placeholder="you@anderson.ucla.edu"
              />
            </Field>
          </div>
        )}

        {step === 2 && (
          <div>
            <p className="font-semibold text-navy-900 mb-4">Where you fit at Anderson</p>
            <Field label="Position">
              <Select value={form.program} onChange={update("program")}>
                {PROGRAMS.map((p) => (
                  <option key={p} value={p}>
                    {p}
                  </option>
                ))}
              </Select>
            </Field>
            <Field label="Section / subdivision">
              <Input value={form.section} onChange={update("section")} placeholder="Section A" />
            </Field>
            <Field label="Country">
              <Input
                value={form.country}
                onChange={update("country")}
                placeholder="United States"
              />
            </Field>
          </div>
        )}

        {step === 3 && (
          <div>
            <p className="font-semibold text-navy-900 mb-1">A little about you</p>
            <p className="text-sm text-navy-500 mb-4">
              This helps us find you an interesting match.
            </p>
            <Field label="Favorite spot in LA">
              <Input
                value={form.favorite_spot_la}
                onChange={update("favorite_spot_la")}
                placeholder="A coffee shop, a hike, a hidden gem..."
              />
            </Field>
            <Field label="What are you most excited about right now?">
              <Textarea
                value={form.excited_about}
                onChange={update("excited_about")}
                placeholder="Could be anything — a class, a trip, a project, a new hobby..."
              />
            </Field>
            <Field label="What's your biggest challenge right now?">
              <Textarea
                value={form.biggest_challenge}
                onChange={update("biggest_challenge")}
                placeholder="Recruiting, a class, navigating LA traffic — whatever's on your mind."
              />
            </Field>
          </div>
        )}

        <div className="flex items-center gap-3 mt-2">
          {step > 1 && (
            <Button variant="secondary" className="flex-1" onClick={() => setStep(step - 1)}>
              Back
            </Button>
          )}
          {step < 3 && (
            <Button className="flex-1" disabled={!stepValid} onClick={() => setStep(step + 1)}>
              Continue
            </Button>
          )}
          {step === 3 && (
            <Button
              className="flex-1"
              disabled={!stepValid}
              loading={loading}
              onClick={handleJoin}
            >
              Join this week's round
            </Button>
          )}
        </div>
      </Card>
    </Screen>
  )
}

export default function SignupScreen({ profile, onSignedUp, onJoinedRound }) {
  if (profile) {
    return <EditProfileForm profile={profile} onSaved={onSignedUp} />
  }
  return <SignupWizard onJoined={onJoinedRound} />
}
