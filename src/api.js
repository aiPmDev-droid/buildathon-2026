async function request(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    throw new Error(data.detail || "Something went wrong")
  }
  return data
}

export function signup(profile) {
  return request("/api/people", {
    method: "POST",
    body: JSON.stringify(profile),
  })
}

export function getPerson(email) {
  return request(`/api/people/${encodeURIComponent(email)}`)
}

export function setOptIn(email, optedIn) {
  return request(`/api/people/${encodeURIComponent(email)}/optin`, {
    method: "POST",
    body: JSON.stringify({ opted_in: optedIn }),
  })
}

export function runRound() {
  return request("/api/rounds/run", { method: "POST" })
}

export function getMatch(email) {
  return request(`/api/matches/${encodeURIComponent(email)}`)
}

export function getMessages(email) {
  return request(`/api/matches/${encodeURIComponent(email)}/messages`)
}

export function sendMessage(email, body) {
  return request(`/api/matches/${encodeURIComponent(email)}/messages`, {
    method: "POST",
    body: JSON.stringify({ body }),
  })
}
