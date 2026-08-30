from dotenv import load_dotenv

load_dotenv(".env.local")

from fastapi import FastAPI, HTTPException  # noqa: E402
from pydantic import BaseModel, EmailStr, Field  # noqa: E402

from . import storage  # noqa: E402
from .icebreaker import build_highlights  # noqa: E402
from .matching import run_matching  # noqa: E402
from .witty import generate_witty_headline  # noqa: E402

app = FastAPI()


class SignupRequest(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    program: str = Field(min_length=1)
    town: str = Field(min_length=1)
    section: str = Field(min_length=1)
    favorite_spot_la: str = Field(min_length=1)
    excited_about: str = Field(min_length=1)
    biggest_challenge: str = Field(min_length=1)


class OptInRequest(BaseModel):
    opted_in: bool


class MessageRequest(BaseModel):
    body: str = Field(min_length=1, max_length=2000)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/people")
def signup(payload: SignupRequest):
    profile = storage.upsert_person(payload.model_dump())
    return profile


@app.get("/api/people/{email}")
def get_person(email: str):
    person = storage.get_person(email)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.post("/api/people/{email}/optin")
def set_opt_in(email: str, payload: OptInRequest):
    person = storage.set_opt_in(email, payload.opted_in)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.post("/api/rounds/run")
def run_round():
    """Runs immediately (on demand, no real scheduler) but each person is
    capped at one new match per rolling week: anyone matched within the
    cooldown window is skipped even if still opted in, so re-running the
    round right after a match doesn't re-match the same people again."""
    people = storage.get_people()
    recently_matched = storage.get_recently_matched_emails()
    opted_in_people = [
        p
        for p in people
        if p.get("opted_in") and p["email"] not in recently_matched
    ]
    existing_matches = storage.get_matches()

    pairs, unmatched = run_matching(opted_in_people, existing_matches)

    round_id = storage.next_round_id()
    storage.append_matches(round_id, pairs)

    all_considered = [p["email"] for p in opted_in_people]
    storage.reset_opt_in_for_emails(all_considered)

    return {
        "round_id": round_id,
        "matched_count": len(pairs) * 2,
        "pair_count": len(pairs),
        "unmatched_count": len(unmatched),
        "pairs": [{"person_a_email": a, "person_b_email": b} for a, b in pairs],
    }


@app.get("/api/matches/{email}")
def latest_match(email: str):
    email_norm = email.strip().lower()
    latest = storage.get_latest_match_for_email(email_norm)
    if latest is None:
        raise HTTPException(status_code=404, detail="No match yet")

    partner_email = (
        latest["person_b_email"]
        if latest["person_a_email"].strip().lower() == email_norm
        else latest["person_a_email"]
    )

    person = storage.get_person(email_norm)
    partner = storage.get_person(partner_email)
    if person is None or partner is None:
        raise HTTPException(status_code=404, detail="Profile missing for match")

    headline = latest.get("headline")
    if not headline:
        # Generated once per match (not per person) and cached, so both sides
        # see the same line and it doesn't regenerate on every page view.
        headline = generate_witty_headline(person, partner)
        storage.set_match_headline(latest["id"], headline)

    highlights = build_highlights(person, partner)

    return {
        "match_id": latest["id"],
        "round_id": latest["round_id"],
        "matched_at": latest["matched_at"],
        "partner": {
            "name": partner["name"],
            "program": partner["program"],
            "favorite_spot_la": partner["favorite_spot_la"],
            "excited_about": partner["excited_about"],
            "biggest_challenge": partner["biggest_challenge"],
        },
        "headline": headline,
        "highlights": highlights,
    }


@app.get("/api/matches/{email}/messages")
def list_messages(email: str):
    latest = storage.get_latest_match_for_email(email)
    if latest is None:
        raise HTTPException(status_code=404, detail="No match yet")
    return storage.get_messages(latest["id"])


@app.post("/api/matches/{email}/messages")
def send_message(email: str, payload: MessageRequest):
    email_norm = email.strip().lower()
    latest = storage.get_latest_match_for_email(email_norm)
    if latest is None:
        raise HTTPException(status_code=404, detail="No match yet")
    return storage.add_message(latest["id"], email_norm, payload.body.strip())
