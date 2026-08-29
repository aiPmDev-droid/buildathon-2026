def _first_name(name: str) -> str:
    return (name or "").strip().split(" ")[0] or "them"


def build_reveal(person: dict, partner: dict) -> dict:
    """AnderMeet deliberately pairs people with little in common, so the
    reveal points at what makes the partner different rather than a shared
    interest — a jumping-off point for the conversation."""
    first = _first_name(partner.get("name"))

    prompts = [
        ("excited_about", f"Ask {first} what they're most excited about right now — they said: “{partner.get('excited_about')}”"),
        ("favorite_spot_la", f"Have them show you their favorite spot in LA — they picked “{partner.get('favorite_spot_la')}”"),
        ("biggest_challenge", f"See if you can help with what they're wrestling with — they mentioned “{partner.get('biggest_challenge')}”"),
    ]
    field, icebreaker = next((p for p in prompts if partner.get(p[0])), prompts[0])

    return {
        "headline": "You two have almost nothing in common — perfect.",
        "icebreaker": icebreaker,
    }
