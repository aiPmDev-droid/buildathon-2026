import confetti from "canvas-confetti"

const CELEBRATED_KEY = "andermeet_celebrated_matches"

function getCelebrated() {
  try {
    return new Set(JSON.parse(localStorage.getItem(CELEBRATED_KEY) || "[]"))
  } catch {
    return new Set()
  }
}

function markCelebrated(matchId) {
  const seen = getCelebrated()
  seen.add(matchId)
  try {
    localStorage.setItem(CELEBRATED_KEY, JSON.stringify([...seen]))
  } catch {
    // best-effort — a missed write just means it might replay once more
  }
}

/** Fires a one-time confetti burst for a given match, scoped to the phone
 * frame (or the full viewport when there's no frame, i.e. on a real phone)
 * so it never spills into the dark backdrop around the device mockup. */
export function celebrateMatch(matchId) {
  if (matchId == null || getCelebrated().has(matchId)) return
  markCelebrated(matchId)

  const frame = document.querySelector(".phone-frame")
  const rect = frame
    ? frame.getBoundingClientRect()
    : { left: 0, top: 0, width: window.innerWidth, height: window.innerHeight }

  const canvas = document.createElement("canvas")
  Object.assign(canvas.style, {
    position: "fixed",
    left: `${rect.left}px`,
    top: `${rect.top}px`,
    width: `${rect.width}px`,
    height: `${rect.height}px`,
    pointerEvents: "none",
    zIndex: 9999,
  })
  document.body.appendChild(canvas)

  const instance = confetti.create(canvas, { resize: false, useWorker: false })
  const colors = ["#ff5d5d", "#ffb02e", "#ffe45e", "#4ade80", "#38bdf8", "#a78bfa", "#f472b6"]

  // Two eruptions from the bottom corners, angled inward and upward — reads
  // as a burst from the bottom rather than confetti just raining down.
  instance({
    particleCount: 60,
    angle: 60,
    spread: 60,
    startVelocity: 55,
    gravity: 0.9,
    ticks: 200,
    origin: { x: 0.1, y: 1 },
    colors,
  })
  instance({
    particleCount: 60,
    angle: 120,
    spread: 60,
    startVelocity: 55,
    gravity: 0.9,
    ticks: 200,
    origin: { x: 0.9, y: 1 },
    colors,
  })
  instance({
    particleCount: 40,
    angle: 90,
    spread: 80,
    startVelocity: 60,
    gravity: 0.9,
    ticks: 200,
    origin: { x: 0.5, y: 1 },
    colors,
  })

  setTimeout(() => canvas.remove(), 4000)
}
