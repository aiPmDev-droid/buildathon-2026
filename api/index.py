from dotenv import load_dotenv

load_dotenv(".env.local")

from fastapi import FastAPI, HTTPException  # noqa: E402
from pydantic import BaseModel, EmailStr, Field  # noqa: E402

from . import storage  # noqa: E402
from .icebreaker import build_reveal  # noqa: E402
from .matching import run_matching  # noqa: E402

app = FastAPI()


class SignupRequest(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    drink: str = Field(min_length=1)
    want_to_learn: str = Field(min_length=1)
    program: str = Field(min_length=1)
    country: str = Field(min_length=1)
    section: str = Field(min_length=1)


class OptInRequest(BaseModel):
    opted_in: bool


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
    people = storage.get_people()
    opted_in_people = [p for p in people if p.get("opted_in")]
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
    matches = storage.get_matches()
    email_norm = email.strip().lower()

    mine = [
        m
        for m in matches
        if m.get("person_a_email", "").strip().lower() == email_norm
        or m.get("person_b_email", "").strip().lower() == email_norm
    ]
    if not mine:
        raise HTTPException(status_code=404, detail="No match yet")

    mine.sort(key=lambda m: m.get("matched_at", ""), reverse=True)
    latest = mine[0]

    partner_email = (
        latest["person_b_email"]
        if latest["person_a_email"].strip().lower() == email_norm
        else latest["person_a_email"]
    )

    person = storage.get_person(email_norm)
    partner = storage.get_person(partner_email)
    if person is None or partner is None:
        raise HTTPException(status_code=404, detail="Profile missing for match")

    reveal = build_reveal(person, partner)

    return {
        "round_id": latest["round_id"],
        "matched_at": latest["matched_at"],
        "partner": {
            "name": partner["name"],
            "program": partner["program"],
            "drink": partner["drink"],
            "want_to_learn": partner["want_to_learn"],
        },
        **reveal,
    }
