import os
from contextlib import contextmanager
from typing import Optional

import psycopg
from psycopg.rows import dict_row

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
            drink TEXT NOT NULL,
            want_to_learn TEXT NOT NULL,
            program TEXT NOT NULL,
            country TEXT NOT NULL,
            section TEXT NOT NULL,
            opted_in BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
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
    _SCHEMA_READY = True


def _serialize_person(row: dict) -> dict:
    return {
        "name": row["name"],
        "email": row["email"],
        "drink": row["drink"],
        "want_to_learn": row["want_to_learn"],
        "program": row["program"],
        "country": row["country"],
        "section": row["section"],
        "opted_in": row["opted_in"],
        "created_at": row["created_at"].isoformat() if row["created_at"] else None,
    }


def _serialize_match(row: dict) -> dict:
    return {
        "round_id": row["round_id"],
        "person_a_email": row["person_a_email"],
        "person_b_email": row["person_b_email"],
        "matched_at": row["matched_at"].isoformat() if row["matched_at"] else None,
    }


def get_people() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM people ORDER BY created_at").fetchall()
        return [_serialize_person(r) for r in rows]


def get_matches() -> list[dict]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT round_id, person_a_email, person_b_email, matched_at "
            "FROM matches ORDER BY matched_at"
        ).fetchall()
        return [_serialize_match(r) for r in rows]


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
            INSERT INTO people (email, name, drink, want_to_learn, program, country, section)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET
                name = EXCLUDED.name,
                drink = EXCLUDED.drink,
                want_to_learn = EXCLUDED.want_to_learn,
                program = EXCLUDED.program,
                country = EXCLUDED.country,
                section = EXCLUDED.section
            RETURNING *
            """,
            (
                email,
                profile["name"],
                profile["drink"],
                profile["want_to_learn"],
                profile["program"],
                profile["country"],
                profile["section"],
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
    if not emails:
        return
    normalized = [e.strip().lower() for e in emails]
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


def next_round_id() -> str:
    with _connect() as conn:
        rows = conn.execute("SELECT DISTINCT round_id FROM matches").fetchall()
    existing = {r["round_id"] for r in rows}
    n = 1
    while str(n) in existing:
        n += 1
    return str(n)
