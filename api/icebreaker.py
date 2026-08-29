def _norm(value: str) -> str:
    return (value or "").strip().lower()


def build_highlights(person: dict, partner: dict) -> list[dict]:
    """AnderMeet deliberately pairs people with nothing in common, so the
    reveal leans into what's DIFFERENT between them — a jumping-off point
    for the conversation — rather than pretending they have things in
    common they don't."""
    diff_fields = [
        ("favorite_spot_la", "Favorite spot in LA"),
        ("excited_about", "What you're excited about"),
        ("biggest_challenge", "Biggest challenge right now"),
    ]

    return [
        {"label": label, "mine": person.get(field), "theirs": partner.get(field)}
        for field, label in diff_fields
        if _norm(person.get(field)) != _norm(partner.get(field)) and partner.get(field)
    ]
