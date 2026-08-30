"""One-time seed script: writes fake people + historical matches to Postgres.

Run from the repo root:
    .venv/bin/python scripts/seed.py

Requires DATABASE_URL in the environment (or a .env.local at the repo root).
Clears and re-seeds the people/matches/messages tables, so it's safe to re-run.
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
    dict(name="Ava Chen", email="ava.chen@anderson.ucla.edu", program="FT MBA",
         town="Chicago", section="A", favorite_spot_la="Griffith Observatory",
         excited_about="Starting my summer internship in fintech",
         biggest_challenge="Deciding on a specialization track"),
    dict(name="Marco Rossi", email="marco.rossi@anderson.ucla.edu", program="FT MBA",
         town="Milan", section="B", favorite_spot_la="Venice Beach boardwalk",
         excited_about="Training for the LA marathon",
         biggest_challenge="Recruiting for consulting while keeping up with case prep"),
    dict(name="Priya Sharma", email="priya.sharma@anderson.ucla.edu", program="FEMBA",
         town="Mumbai", section="A", favorite_spot_la="Grand Central Market",
         excited_about="Launching a side project with a classmate",
         biggest_challenge="Balancing FEMBA classes with a full-time job"),
    dict(name="Diego Fernandez", email="diego.fernandez@anderson.ucla.edu", program="FT MBA",
         town="Mexico City", section="C", favorite_spot_la="Elysian Park",
         excited_about="A rock climbing trip to Joshua Tree",
         biggest_challenge="Getting through accounting without a finance background"),
    dict(name="Wei Zhang", email="wei.zhang@anderson.ucla.edu", program="PhD",
         town="Beijing", section="B", favorite_spot_la="Huntington Library gardens",
         excited_about="A paper getting accepted to a conference",
         biggest_challenge="Writing the literature review chapter"),
    dict(name="Sofia Kowalski", email="sofia.kowalski@anderson.ucla.edu", program="FEMBA",
         town="Warsaw", section="C", favorite_spot_la="Abbot Kinney Blvd",
         excited_about="A sailing trip out of Marina del Rey",
         biggest_challenge="Finding time to study for the GMAT retake"),
    dict(name="James Okafor", email="james.okafor@anderson.ucla.edu", program="FT MBA",
         town="Lagos", section="A", favorite_spot_la="LACMA",
         excited_about="Visiting family for the first time in a year",
         biggest_challenge="Navigating LA traffic to make it to recruiting events"),
    dict(name="Elena Petrova", email="elena.petrova@anderson.ucla.edu", program="FT MBA",
         town="Moscow", section="B", favorite_spot_la="Runyon Canyon",
         excited_about="A case competition in San Francisco next month",
         biggest_challenge="Networking as an introvert"),
    dict(name="Lucas Silva", email="lucas.silva@anderson.ucla.edu", program="FEMBA",
         town="São Paulo", section="C", favorite_spot_la="Santa Monica Pier",
         excited_about="Learning to surf this quarter",
         biggest_challenge="Making time for electives outside my track"),
    dict(name="Hannah Kim", email="hannah.kim@anderson.ucla.edu", program="PhD",
         town="Seoul", section="A", favorite_spot_la="Koreatown night markets",
         excited_about="Defending my dissertation proposal",
         biggest_challenge="Finding participants for my research study"),
    # These two are never part of a historical match and sit in their own
    # section/town, distinct from everyone else — so a fresh reseed always
    # has at least one guaranteed-valid, never-before-matched pair available
    # immediately, regardless of what happens to the other 10 during a demo.
    dict(name="Nora Fischer", email="nora.fischer@anderson.ucla.edu", program="MSBA",
         town="Berlin", section="D", favorite_spot_la="Descanso Gardens",
         excited_about="Starting a new rotation on the analytics team",
         biggest_challenge="Picking electives for next quarter"),
    dict(name="Omar Haddad", email="omar.haddad@anderson.ucla.edu", program="MFE",
         town="Dubai", section="E", favorite_spot_la="The Getty Center",
         excited_about="A ski trip to Mammoth this winter",
         biggest_challenge="Keeping up with the stochastic calculus problem sets"),
    # Demo safety net (see storage.ALWAYS_AVAILABLE_EMAILS): exempt from the
    # rematch cooldown and never opted out, so a live tester can always get
    # a match. They're also hard-excluded from pairing with each other (see
    # matching.py), so they can never "use each other up" -- three of them
    # (odd count) gives headroom for multiple real testers matching
    # concurrently, on top of the single-tester guarantee two already gave.
    dict(name="Sam Whitfield", email="sam.whitfield@anderson.ucla.edu", program="Faculty/Staff",
         town="Reykjavik", section="ZZ1", favorite_spot_la="The Last Bookstore",
         excited_about="Mentoring first-years this quarter",
         biggest_challenge="Balancing teaching load with committee work"),
    dict(name="Jordan Blake", email="jordan.blake@anderson.ucla.edu", program="MFE",
         town="Nairobi", section="ZZ2", favorite_spot_la="Malibu Pier",
         excited_about="Training for a triathlon this spring",
         biggest_challenge="Derivatives pricing problem sets"),
    dict(name="Taylor Osei", email="taylor.osei@anderson.ucla.edu", program="EMBA",
         town="Wellington", section="ZZ3", favorite_spot_la="Echo Park Lake",
         excited_about="A half-marathon along the LA river trail",
         biggest_challenge="Fitting case prep in around a full-time job"),
]

# (person_a, person_b, round_id, days_ago) — all opposite section/town,
# so they were valid pairs *at the time*. Seeding them into "matches" means
# the live matching round won't repeat them, and (being older than the
# 7-day cooldown) won't block them from being eligible for a new match now.
HISTORICAL_ROUNDS = [
    ("ava.chen@anderson.ucla.edu", "marco.rossi@anderson.ucla.edu", "1", 28),
    ("james.okafor@anderson.ucla.edu", "wei.zhang@anderson.ucla.edu", "1", 28),
    ("diego.fernandez@anderson.ucla.edu", "elena.petrova@anderson.ucla.edu", "2", 14),
    ("lucas.silva@anderson.ucla.edu", "hannah.kim@anderson.ucla.edu", "3", 9),
]


def main():
    with storage._connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM messages")
            cur.execute("DELETE FROM matches")
            cur.execute("DELETE FROM people")

            for p in PEOPLE:
                cur.execute(
                    """
                    INSERT INTO people
                        (email, name, program, town, section,
                         favorite_spot_la, excited_about, biggest_challenge,
                         opted_in, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        p["email"].lower(),
                        p["name"],
                        p["program"],
                        p["town"],
                        p["section"],
                        p["favorite_spot_la"],
                        p["excited_about"],
                        p["biggest_challenge"],
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
