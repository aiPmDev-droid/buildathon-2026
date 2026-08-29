def _first_name(name: str) -> str:
    return (name or "").strip().split(" ")[0] or "them"


def _norm(value: str) -> str:
    return (value or "").strip().lower()


def build_reveal(person: dict, partner: dict) -> dict:
    """AnderMeet deliberately pairs people with little in common, so the
    reveal leans into what's DIFFERENT between them — a jumping-off point
    for the conversation — rather than pretending they have things in
    common they don't."""
    first = _first_name(partner.get("name"))

    diff_fields = [
        ("favorite_spot_la", "Favorite spot in LA"),
        ("excited_about", "What you're excited about"),
        ("biggest_challenge", "Biggest challenge right now"),
    ]

    highlights = []
    for field, label in diff_fields:
        mine, theirs = person.get(field), partner.get(field)
        if _norm(mine) != _norm(theirs) and theirs:
            highlights.append(f"{label} — you: “{mine}” · {first}: “{theirs}”")

    if not highlights:
        highlights.append(f"You and {first} answered almost identically — rare, and worth comparing notes on.")

    prompts = [
        ("excited_about", f"Ask {first} what they're most excited about right now — they said: “{partner.get('excited_about')}”"),
        ("favorite_spot_la", f"Have them show you their favorite spot in LA — they picked “{partner.get('favorite_spot_la')}”"),
        ("biggest_challenge", f"See if you can help with what they're wrestling with — they mentioned “{partner.get('biggest_challenge')}”"),
    ]
    _, icebreaker = next((p for p in prompts if partner.get(p[0])), prompts[0])

    return {
        "headline": "You two have almost nothing in common — perfect.",
        "highlights": highlights,
        "icebreaker": icebreaker,
    }
