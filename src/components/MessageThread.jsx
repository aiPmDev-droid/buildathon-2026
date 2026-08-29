import { useEffect, useRef, useState } from "react"
import { getMessages, sendMessage } from "../api"

export default function MessageThread({ email, matchId, partnerFirstName }) {
  const [messages, setMessages] = useState([])
  const [text, setText] = useState("")
  const [sending, setSending] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    let cancelled = false
    const load = () => {
      getMessages(email)
        .then((msgs) => {
          if (!cancelled) setMessages(msgs)
        })
        .catch(() => {})
    }
    load()
    const interval = setInterval(load, 4000)
    return () => {
      cancelled = true
      clearInterval(interval)
    }
  }, [email, matchId])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" })
  }, [messages.length])

  const handleSend = async (e) => {
    e.preventDefault()
    const body = text.trim()
    if (!body) return
    setSending(true)
    try {
      const msg = await sendMessage(email, body)
      setMessages((m) => [...m, msg])
      setText("")
    } catch {
      // best-effort for the prototype
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="mt-4">
      <p className="text-xs uppercase tracking-wide text-navy-400 font-medium mb-2">
        Text {partnerFirstName}
      </p>
      <div className="rounded-2xl border border-navy-100 bg-white overflow-hidden">
        <div className="max-h-64 overflow-y-auto p-3 space-y-2">
          {messages.length === 0 && (
            <p className="text-sm text-navy-300 text-center py-6">No messages yet — say hi!</p>
          )}
          {messages.map((m) => {
            const mine = m.sender_email === email
            return (
              <div key={m.id} className={`flex ${mine ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[75%] rounded-2xl px-3.5 py-2 text-sm leading-snug break-words ${
                    mine
                      ? "bg-navy-700 text-white rounded-br-sm"
                      : "bg-navy-50 text-navy-900 rounded-bl-sm"
                  }`}
                >
                  {m.body}
                </div>
              </div>
            )
          })}
          <div ref={bottomRef} />
        </div>
        <form
          onSubmit={handleSend}
          className="flex items-center gap-2 border-t border-navy-100 p-2"
        >
          <input
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type a message…"
            className="flex-1 rounded-full bg-navy-50 px-4 py-2 text-sm outline-none focus:ring-2 focus:ring-accent-400/30"
          />
          <button
            type="submit"
            disabled={sending || !text.trim()}
            className="h-9 w-9 shrink-0 rounded-full bg-navy-700 text-white flex items-center justify-center disabled:opacity-40 transition-opacity"
            aria-label="Send"
          >
            ➤
          </button>
        </form>
      </div>
    </div>
  )
}
