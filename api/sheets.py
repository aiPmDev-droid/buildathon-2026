import json
import os
from datetime import datetime, timezone
from functools import lru_cache

import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

PEOPLE_HEADERS = [
    "name",
    "email",
    "drink",
    "want_to_learn",
    "program",
    "country",
    "section",
    "opted_in",
    "created_at",
]
MATCHES_HEADERS = ["round_id", "person_a_email", "person_b_email", "matched_at"]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _truthy(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().upper() in ("TRUE", "YES", "1")


@lru_cache(maxsize=1)
def _client() -> gspread.Client:
    raw = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    info = json.loads(raw)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return gspread.authorize(creds)


@lru_cache(maxsize=1)
def _spreadsheet():
    return _client().open_by_key(os.environ["GOOGLE_SHEET_ID"])


def _worksheet(title: str, headers: list[str]):
    sh = _spreadsheet()
    try:
        ws = sh.worksheet(title)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=title, rows=200, cols=len(headers) + 2)
        ws.append_row(headers, value_input_option="USER_ENTERED")
        return ws
    existing = ws.row_values(1)
    if existing != headers:
        ws.update("A1", [headers])
    return ws


def people_ws():
    return _worksheet("People", PEOPLE_HEADERS)


def matches_ws():
    return _worksheet("Matches", MATCHES_HEADERS)


def get_people() -> list[dict]:
    records = people_ws().get_all_records(expected_headers=PEOPLE_HEADERS)
    for r in records:
        r["opted_in"] = _truthy(r.get("opted_in"))
    return records


def get_matches() -> list[dict]:
    return matches_ws().get_all_records(expected_headers=MATCHES_HEADERS)


def _find_person_row(email: str):
    ws = people_ws()
    col_values = ws.col_values(2)  # email is column B
    email_norm = email.strip().lower()
    for idx, val in enumerate(col_values[1:], start=2):
        if val.strip().lower() == email_norm:
            return ws, idx
    return ws, None


def upsert_person(profile: dict) -> dict:
    email = profile["email"].strip().lower()
    ws, row_idx = _find_person_row(email)

    if row_idx is None:
        row = [
            profile["name"],
            email,
            profile["drink"],
            profile["want_to_learn"],
            profile["program"],
            profile["country"],
            profile["section"],
            "FALSE",
            now_iso(),
        ]
        ws.append_row(row, value_input_option="USER_ENTERED")
        profile = {**profile, "email": email, "opted_in": False, "created_at": row[-1]}
        return profile

    existing = ws.row_values(row_idx)
    created_at = existing[8] if len(existing) > 8 else now_iso()
    opted_in = existing[7] if len(existing) > 7 else "FALSE"
    row = [
        profile["name"],
        email,
        profile["drink"],
        profile["want_to_learn"],
        profile["program"],
        profile["country"],
        profile["section"],
        opted_in,
        created_at,
    ]
    ws.update(f"A{row_idx}:I{row_idx}", [row], value_input_option="USER_ENTERED")
    return {**profile, "email": email, "opted_in": _truthy(opted_in), "created_at": created_at}


def get_person(email: str) -> dict | None:
    ws, row_idx = _find_person_row(email)
    if row_idx is None:
        return None
    values = ws.row_values(row_idx)
    values += [""] * (len(PEOPLE_HEADERS) - len(values))
    record = dict(zip(PEOPLE_HEADERS, values))
    record["opted_in"] = _truthy(record.get("opted_in"))
    return record


def set_opt_in(email: str, opted_in: bool) -> dict | None:
    ws, row_idx = _find_person_row(email)
    if row_idx is None:
        return None
    ws.update_cell(row_idx, 8, "TRUE" if opted_in else "FALSE")  # opted_in is column H
    return get_person(email)


def reset_opt_in_for_emails(emails: list[str]) -> None:
    if not emails:
        return
    ws = people_ws()
    col_values = ws.col_values(2)
    targets = {e.strip().lower() for e in emails}
    updates = []
    for idx, val in enumerate(col_values[1:], start=2):
        if val.strip().lower() in targets:
            updates.append({"range": f"H{idx}", "values": [["FALSE"]]})
    if updates:
        ws.batch_update(updates, value_input_option="USER_ENTERED")


def append_matches(round_id: str, pairs: list[tuple[str, str]]) -> None:
    if not pairs:
        return
    matched_at = now_iso()
    rows = [[round_id, a, b, matched_at] for a, b in pairs]
    matches_ws().append_rows(rows, value_input_option="USER_ENTERED")


def next_round_id() -> str:
    matches = get_matches()
    existing = {m["round_id"] for m in matches if m.get("round_id")}
    n = 1
    while str(n) in existing:
        n += 1
    return str(n)
