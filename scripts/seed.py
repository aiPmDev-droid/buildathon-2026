"""One-time seed script: writes fake people + historical matches to Redis.

Run from the repo root:
    .venv/bin/python scripts/seed.py

Requires UPSTASH_REDIS_REST_URL / UPSTASH_REDIS_REST_TOKEN in the
environment (or a .env.local at the repo root).
"""

import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(".env.local")

from api import storage  # noqa: E402

NOW = datetime.now(timezone.utc)


def days_ago(n: int) -> str:
    return (NOW - timedelta(days=n)).isoformat()


PEOPLE = [
    dict(name="Ava Chen", email="ava.chen@anderson.ucla.edu", drink="Oat milk latte",
         want_to_learn="Salsa dancing", program="FT MBA", country="United States", section="A"),
    dict(name="Marco Rossi", email="marco.rossi@anderson.ucla.edu", drink="Espresso",
         want_to_learn="Sailing", program="FT MBA", country="Italy", section="B"),
    dict(name="Priya Sharma", email="priya.sharma@anderson.ucla.edu", drink="Chai latte",
         want_to_learn="Salsa dancing", program="FEMBA", country="India", section="A"),
    dict(name="Diego Fernandez", email="diego.fernandez@anderson.ucla.edu", drink="Cold brew",
         want_to_learn="Rock climbing", program="FT MBA", country="Mexico", section="C"),
    dict(name="Wei Zhang", email="wei.zhang@anderson.ucla.edu", drink="Oat milk latte",
         want_to_learn="Photography", program="PhD", country="China", section="B"),
    dict(name="Sofia Kowalski", email="sofia.kowalski@anderson.ucla.edu", drink="Cappuccino",
         want_to_learn="Sailing", program="FEMBA", country="Poland", section="C"),
    dict(name="James Okafor", email="james.okafor@anderson.ucla.edu", drink="Espresso",
         want_to_learn="Wine tasting", program="FT MBA", country="Nigeria", section="A"),
    dict(name="Elena Petrova", email="elena.petrova@anderson.ucla.edu", drink="Cold brew",
         want_to_learn="Rock climbing", program="FT MBA", country="Russia", section="B"),
    dict(name="Lucas Silva", email="lucas.silva@anderson.ucla.edu", drink="Chai latte",
         want_to_learn="Photography", program="FEMBA", country="Brazil", section="C"),
    dict(name="Hannah Kim", email="hannah.kim@anderson.ucla.edu", drink="Cappuccino",
         want_to_learn="Wine tasting", program="PhD", country="South Korea", section="A"),
]

# (person_a, person_b, round_id, days_ago) — all opposite section/country,
# so they were valid pairs *at the time*. Seeding them into "matches" means
# the live matching round won't repeat them.
HISTORICAL_ROUNDS = [
    ("ava.chen@anderson.ucla.edu", "marco.rossi@anderson.ucla.edu", "1", 28),
    ("james.okafor@anderson.ucla.edu", "wei.zhang@anderson.ucla.edu", "1", 28),
    ("diego.fernandez@anderson.ucla.edu", "elena.petrova@anderson.ucla.edu", "2", 14),
    ("lucas.silva@anderson.ucla.edu", "hannah.kim@anderson.ucla.edu", "3", 7),
]


def main():
    people = [
        {**p, "email": p["email"].lower(), "opted_in": True, "created_at": days_ago(30)}
        for p in PEOPLE
    ]
    storage._write_list(storage.PEOPLE_KEY, people)
    print(f"Seeded {len(people)} people.")

    matches = [
        {
            "round_id": round_id,
            "person_a_email": a,
            "person_b_email": b,
            "matched_at": days_ago(age),
        }
        for a, b, round_id, age in HISTORICAL_ROUNDS
    ]
    storage._write_list(storage.MATCHES_KEY, matches)
    print(f"Seeded {len(matches)} historical matches across "
          f"{len({m['round_id'] for m in matches})} rounds.")


if __name__ == "__main__":
    main()
