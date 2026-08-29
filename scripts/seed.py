"""One-time seed script: writes fake people + historical matches to Postgres.

Run from the repo root:
    .venv/bin/python scripts/seed.py

Requires DATABASE_URL in the environment (or a .env.local at the repo root).
Clears and re-seeds the people/matches tables, so it's safe to re-run.
"""

import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(".env.local")

from api import storage  # noqa: E402

NOW = datetime.now(timezone.utc)


def days_ago(n: int) -> datetime:
    return NOW - timedelta(days=n)


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
    with storage._connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM matches")
            cur.execute("DELETE FROM people")

            for p in PEOPLE:
                cur.execute(
                    """
                    INSERT INTO people
                        (email, name, drink, want_to_learn, program, country, section,
                         opted_in, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        p["email"].lower(),
                        p["name"],
                        p["drink"],
                        p["want_to_learn"],
                        p["program"],
                        p["country"],
                        p["section"],
                        True,
                        days_ago(30),
                    ),
                )
            print(f"Seeded {len(PEOPLE)} people.")

            for a, b, round_id, age in HISTORICAL_ROUNDS:
                cur.execute(
                    """
                    INSERT INTO matches (round_id, person_a_email, person_b_email, matched_at)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (round_id, a, b, days_ago(age)),
                )
            rounds = len({r[2] for r in HISTORICAL_ROUNDS})
            print(f"Seeded {len(HISTORICAL_ROUNDS)} historical matches across {rounds} rounds.")


if __name__ == "__main__":
    main()
