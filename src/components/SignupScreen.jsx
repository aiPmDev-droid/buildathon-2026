import { useState } from "react"
import { signup } from "../api"
import { Screen, Card, Field, Input, Button, Toast } from "./ui"

const EMPTY = {
  name: "",
  email: "",
  drink: "",
  want_to_learn: "",
  program: "",
  country: "",
  section: "",
}

export default function SignupScreen({ profile, onSignedUp }) {
  const [form, setForm] = useState(profile || EMPTY)
  const [loading, setLoading] = useState(false)
  const [toast, setToast] = useState(null)

  const isEditing = Boolean(profile)

  const update = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setToast(null)
    try {
      const saved = await signup(form)
      onSignedUp(saved)
      setToast({ message: isEditing ? "Profile updated" : "You're signed up ☕", tone: "success" })
    } catch (err) {
      setToast({ message: err.message, tone: "error" })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Screen
      title="Coffee Roulette"
      subtitle={isEditing ? "Your profile" : "Sign up for UCLA Anderson coffee chats"}
    >
      <Toast {...toast} />
      <Card>
        <form onSubmit={handleSubmit}>
          <Field label="Name">
            <Input
              required
              value={form.name}
              onChange={update("name")}
              placeholder="Jane Bruin"
            />
          </Field>
          <Field label="Email">
            <Input
              required
              type="email"
              value={form.email}
              onChange={update("email")}
              placeholder="jane.bruin.mba2027@anderson.ucla.edu"
              disabled={isEditing}
            />
          </Field>
          <Field label="Favorite drink">
            <Input
              required
              value={form.drink}
              onChange={update("drink")}
              placeholder="Oat milk latte"
            />
          </Field>
          <Field label="Something you'd like to learn">
            <Input
              required
              value={form.want_to_learn}
              onChange={update("want_to_learn")}
              placeholder="Salsa dancing, sailing, sourdough..."
            />
          </Field>
          <Field label="Program / position">
            <Input
              required
              value={form.program}
              onChange={update("program")}
              placeholder="FEMBA, FT MBA, PhD..."
            />
          </Field>
          <Field label="Country">
            <Input
              required
              value={form.country}
              onChange={update("country")}
              placeholder="United States"
            />
          </Field>
          <Field label="Section">
            <Input required value={form.section} onChange={update("section")} placeholder="A" />
          </Field>
          <Button type="submit" loading={loading} className="mt-2">
            {isEditing ? "Save changes" : "Sign up"}
          </Button>
        </form>
      </Card>
    </Screen>
  )
}
