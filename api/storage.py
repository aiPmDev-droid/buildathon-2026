import json
import os
from datetime import datetime, timezone
from functools import lru_cache

from upstash_redis import Redis

PEOPLE_KEY = "people"
MATCHES_KEY = "matches"

PERSON_FIELDS = [
    "name",
    "email",
    "drink",
    "want_to_learn",
    "program",
    "country",
    "section",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@lru_cache(maxsize=1)
def _redis() -> Redis:
    return Redis(
        url=os.environ["UPSTASH_REDIS_REST_URL"],
        token=os.environ["UPSTASH_REDIS_REST_TOKEN"],
    )


def _read_list(key: str) -> list[dict]:
    raw = _redis().get(key)
    if not raw:
        return []
    return json.loads(raw)


def _write_list(key: str, items: list[dict]) -> None:
    _redis().set(key, json.dumps(items))


def get_people() -> list[dict]:
    return _read_list(PEOPLE_KEY)


def get_matches() -> list[dict]:
    return _read_list(MATCHES_KEY)


def _find_person_index(people: list[dict], email: str):
    email_norm = email.strip().lower()
    for i, p in enumerate(people):
        if p.get("email", "").strip().lower() == email_norm:
            return i
    return None


def get_person(email: str) -> dict | None:
    people = get_people()
    idx = _find_person_index(people, email)
    return people[idx] if idx is not None else None


def upsert_person(profile: dict) -> dict:
    people = get_people()
    email = profile["email"].strip().lower()
    idx = _find_person_index(people, email)
    fields = {k: profile[k] for k in PERSON_FIELDS if k != "email"}

    if idx is None:
        record = {
            "email": email,
            **fields,
            "opted_in": False,
            "created_at": now_iso(),
        }
        people.append(record)
    else:
        existing = people[idx]
        record = {
            "email": email,
            **fields,
            "opted_in": existing.get("opted_in", False),
            "created_at": existing.get("created_at", now_iso()),
        }
        people[idx] = record

    _write_list(PEOPLE_KEY, people)
    return record


def set_opt_in(email: str, opted_in: bool) -> dict | None:
    people = get_people()
    idx = _find_person_index(people, email)
    if idx is None:
        return None
    people[idx]["opted_in"] = opted_in
    _write_list(PEOPLE_KEY, people)
    return people[idx]


def reset_opt_in_for_emails(emails: list[str]) -> None:
    if not emails:
        return
    targets = {e.strip().lower() for e in emails}
    people = get_people()
    changed = False
    for p in people:
        if p.get("email", "").strip().lower() in targets and p.get("opted_in"):
            p["opted_in"] = False
            changed = True
    if changed:
        _write_list(PEOPLE_KEY, people)


def append_matches(round_id: str, pairs: list[tuple[str, str]]) -> None:
    if not pairs:
        return
    matched_at = now_iso()
    matches = get_matches()
    for a, b in pairs:
        matches.append(
            {
                "round_id": round_id,
                "person_a_email": a,
                "person_b_email": b,
                "matched_at": matched_at,
            }
        )
    _write_list(MATCHES_KEY, matches)


def next_round_id() -> str:
    matches = get_matches()
    existing = {m["round_id"] for m in matches if m.get("round_id")}
    n = 1
    while str(n) in existing:
        n += 1
    return str(n)
