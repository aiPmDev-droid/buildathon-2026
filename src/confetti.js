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

  const instance = confetti.create(canvas, { resize: false, useWorker: true })
  instance({
    particleCount: 90,
    spread: 70,
    startVelocity: 35,
    origin: { y: 0.35 },
    colors: ["#2c5372", "#3d6a90", "#6690b3", "#5f88a0", "#f7f5f0"],
  })

  setTimeout(() => canvas.remove(), 3500)
}
