import os
from contextlib import contextmanager
from typing import Optional

import psycopg
from psycopg.rows import dict_row

REMATCH_COOLDOWN_DAYS = 7

# Demo safety net: these profiles are always eligible for a new round,
# bypassing the rematch cooldown, and never get their opt-in reset. So
# whoever tests the app (e.g. a judge) can always get a live match,
# regardless of who else has already been paired up recently.
ALWAYS_AVAILABLE_EMAILS = {
    "sam.whitfield@anderson.ucla.edu",
    "jordan.blake@anderson.ucla.edu",
    "taylor.osei@anderson.ucla.edu",
}

_SCHEMA_READY = False


@contextmanager
def _connect():
    conn = psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row, autocommit=True)
    try:
        _ensure_schema(conn)
        yield conn
    finally:
        conn.close()


def _ensure_schema(conn) -> None:
    global _SCHEMA_READY
    if _SCHEMA_READY:
        return
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS people (
            email TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            program TEXT NOT NULL,
            town TEXT NOT NULL,
            section TEXT NOT NULL,
            favorite_spot_la TEXT NOT NULL,
            excited_about TEXT NOT NULL,
            biggest_challenge TEXT NOT NULL,
            opted_in BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    # Cooldown is tracked here, separately from the `matches` table, on
    # purpose: `matches` is the permanent "have these two ever been paired"
    # record and must never be edited to manage cooldown, or the never-repeat
    # guarantee breaks (this bit us once — see reset_cooldown_for_all).
    conn.execute("ALTER TABLE people ADD COLUMN IF NOT EXISTS last_matched_at TIMESTAMPTZ")
    conn.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'people' AND column_name = 'city'
            ) THEN
                ALTER TABLE people RENAME COLUMN city TO town;
            END IF;
        END $$;
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS matches (
            id SERIAL PRIMARY KEY,
            round_id TEXT NOT NULL,
            person_a_email TEXT NOT NULL REFERENCES people(email),
            person_b_email TEXT NOT NULL REFERENCES people(email),
            matched_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    conn.execute("ALTER TABLE matches ADD COLUMN IF NOT EXISTS headline TEXT")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            match_id INTEGER NOT NULL REFERENCES matches(id),
            sender_email TEXT NOT NULL,
            body TEXT NOT NULL,
            sent_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    _SCHEMA_READY = True


PERSON_FIELDS = [
    "name",
    "program",
    "town",
    "section",
    "favorite_spot_la",
    "excited_about",
    "biggest_challenge",
]


def _serialize_person(row: dict) -> dict:
    return {
        "email": row["email"],
        **{f: row[f] for f in PERSON_FIELDS},
        "opted_in": row["opted_in"],
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
    }


def _serialize_match(row: dict) -> dict:
    return {
        "id": row["id"],
        "round_id": row["round_id"],
        "person_a_email": row["person_a_email"],
        "person_b_email": row["person_b_email"],
        "matched_at": row["matched_at"].isoformat() if row["matched_at"] else None,
        "headline": row.get("headline"),
    }


def _serialize_message(row: dict) -> dict:
    return {
        "id": row["id"],
        "match_id": row["match_id"],
        "sender_email": row["sender_email"],
        "body": row["body"],
        "sent_at": row["sent_at"].isoformat() if row["sent_at"] else None,
    }


def get_people() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM people ORDER BY created_at").fetchall()
        return [_serialize_person(r) for r in rows]


def get_matches() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, round_id, person_a_email, person_b_email, matched_at, headline "
            "FROM matches ORDER BY matched_at"
        ).fetchall()
        return [_serialize_match(r) for r in rows]


def get_recently_matched_emails(within_days: int = REMATCH_COOLDOWN_DAYS) -> set[str]:
    """Emails ineligible for a new round because they were matched within the
    cooldown window, even if still opted in. Reads people.last_matched_at,
    NOT the matches table — cooldown and match history are intentionally
    separate so clearing one can never corrupt the other."""
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT email FROM people
            WHERE last_matched_at > now() - (%s || ' days')::interval
            """,
            (within_days,),
        ).fetchall()
    return {r["email"] for r in rows}


def reset_cooldown_for_all() -> None:
    """Clears the rematch cooldown for every person, for demo purposes.
    Only touches people.last_matched_at — never deletes from `matches`,
    which stays the permanent, untouchable record of who's already been
    paired with whom."""
    with _connect() as conn:
        conn.execute("UPDATE people SET last_matched_at = NULL")


def get_person(email: str) -> Optional[dict]:
    email = email.strip().lower()
    with _connect() as conn:
        row = conn.execute("SELECT * FROM people WHERE email = %s", (email,)).fetchone()
        return _serialize_person(row) if row else None


def upsert_person(profile: dict) -> dict:
    email = profile["email"].strip().lower()
    with _connect() as conn:
        row = conn.execute(
            """
            INSERT INTO people
                (email, name, program, town, section,
                 favorite_spot_la, excited_about, biggest_challenge)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET
                name = EXCLUDED.name,
                program = EXCLUDED.program,
                town = EXCLUDED.town,
                section = EXCLUDED.section,
                favorite_spot_la = EXCLUDED.favorite_spot_la,
                excited_about = EXCLUDED.excited_about,
                biggest_challenge = EXCLUDED.biggest_challenge
            RETURNING *
            """,
            (
                email,
                profile["name"],
                profile["program"],
                profile["town"],
                profile["section"],
                profile["favorite_spot_la"],
                profile["excited_about"],
                profile["biggest_challenge"],
            ),
        ).fetchone()
        return _serialize_person(row)


def set_opt_in(email: str, opted_in: bool) -> Optional[dict]:
    email = email.strip().lower()
    with _connect() as conn:
        row = conn.execute(
            "UPDATE people SET opted_in = %s WHERE email = %s RETURNING *",
            (opted_in, email),
        ).fetchone()
        return _serialize_person(row) if row else None


def reset_opt_in_for_emails(emails: list[str]) -> None:
    normalized = [e.strip().lower() for e in emails if e.strip().lower() not in ALWAYS_AVAILABLE_EMAILS]
    if not normalized:
        return
    with _connect() as conn:
        conn.execute("UPDATE people SET opted_in = FALSE WHERE email = ANY(%s)", (normalized,))


def append_matches(round_id: str, pairs: list[tuple[str, str]]) -> None:
    if not pairs:
        return
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO matches (round_id, person_a_email, person_b_email) "
                "VALUES (%s, %s, %s)",
                [(round_id, a, b) for a, b in pairs],
            )
        matched_emails = {email for pair in pairs for email in pair}
        conn.execute(
            "UPDATE people SET last_matched_at = now() WHERE email = ANY(%s)",
            (list(matched_emails),),
        )


def next_round_id() -> str:
    with _connect() as conn:
        rows = conn.execute("SELECT DISTINCT round_id FROM matches").fetchall()
    existing = {r["round_id"] for r in rows}
    n = 1
    while str(n) in existing:
        n += 1
    return str(n)


def get_latest_match_for_email(email: str) -> Optional[dict]:
    email = email.strip().lower()
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT id, round_id, person_a_email, person_b_email, matched_at, headline
            FROM matches
            WHERE person_a_email = %s OR person_b_email = %s
            ORDER BY matched_at DESC
            LIMIT 1
            """,
            (email, email),
        ).fetchone()
    return _serialize_match(row) if row else None


def set_match_headline(match_id: int, headline: str) -> None:
    with _connect() as conn:
        conn.execute(
            "UPDATE matches SET headline = %s WHERE id = %s",
            (headline, match_id),
        )


def get_messages(match_id: int) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT * FROM messages WHERE match_id = %s ORDER BY sent_at",
            (match_id,),
        ).fetchall()
    return [_serialize_message(r) for r in rows]


def add_message(match_id: int, sender_email: str, body: str) -> dict:
    sender_email = sender_email.strip().lower()
    with _connect() as conn:
        row = conn.execute(
            """
            INSERT INTO messages (match_id, sender_email, body)
            VALUES (%s, %s, %s)
            RETURNING *
            """,
            (match_id, sender_email, body),
        ).fetchone()
    return _serialize_message(row)
