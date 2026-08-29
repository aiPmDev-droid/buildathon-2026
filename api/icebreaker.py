def _norm(value: str) -> str:
    return (value or "").strip().lower()


def build_reveal(person: dict, partner: dict) -> dict:
    """Returns {shared_interest, icebreaker} describing why person + partner were paired."""
    p_learn, partner_learn = _norm(person.get("want_to_learn")), _norm(partner.get("want_to_learn"))
    p_drink, partner_drink = _norm(person.get("drink")), _norm(partner.get("drink"))

    if p_learn and p_learn == partner_learn:
        topic = person.get("want_to_learn")
        return {
            "shared_interest": f"You both want to learn {topic}",
            "icebreaker": f"Trade notes on {topic} — who's further along, and what got you into it?",
        }
    if p_drink and p_drink == partner_drink:
        drink = person.get("drink")
        return {
            "shared_interest": f"You're both {drink} people",
            "icebreaker": f"Order the same {drink} and settle it: who found the better spot for one near campus?",
        }
    return {
        "shared_interest": "A fresh connection",
        "icebreaker": "No overlap on file yet — good excuse to find one over coffee. Ask what they'd want to learn next.",
    }
