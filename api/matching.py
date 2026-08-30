import random

from .storage import ALWAYS_AVAILABLE_EMAILS


def _norm(value: str) -> str:
    return (value or "").strip().lower()


def _already_matched_pairs(existing_matches: list[dict]) -> set[frozenset]:
    pairs = set()
    for m in existing_matches:
        a = _norm(m.get("person_a_email"))
        b = _norm(m.get("person_b_email"))
        if a and b:
            pairs.add(frozenset({a, b}))
    return pairs


def run_matching(
    opted_in_people: list[dict], existing_matches: list[dict]
) -> tuple[list[tuple[str, str]], list[str]]:
    """Greedily pair opted-in people. A pair is only eligible if they're in a
    different program, section, and town before Anderson (people who likely
    already know each other), and have never been matched before. Shared
    interests are fine, not excluded: any overlap in their answers is just
    material for the witty match-reveal line, not something to avoid.
    """
    people = [p for p in opted_in_people if p.get("email")]
    random.shuffle(people)  # vary assignment order between runs

    already_matched = _already_matched_pairs(existing_matches)

    candidate_pairs = []
    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            p1, p2 = people[i], people[j]
            e1, e2 = _norm(p1["email"]), _norm(p2["email"])
            if e1 in ALWAYS_AVAILABLE_EMAILS and e2 in ALWAYS_AVAILABLE_EMAILS:
                continue  # fallback profiles must never "use each other up"
            if frozenset({e1, e2}) in already_matched:
                continue
            program1, program2 = _norm(p1.get("program")), _norm(p2.get("program"))
            if program1 and program1 == program2:
                continue
            section1, section2 = _norm(p1.get("section")), _norm(p2.get("section"))
            if section1 and section1 == section2:
                continue
            town1, town2 = _norm(p1.get("town")), _norm(p2.get("town"))
            if town1 and town1 == town2:
                continue
            candidate_pairs.append((e1, e2))

    assigned: set[str] = set()
    result_pairs: list[tuple[str, str]] = []
    for e1, e2 in candidate_pairs:
        if e1 in assigned or e2 in assigned:
            continue
        result_pairs.append((e1, e2))
        assigned.add(e1)
        assigned.add(e2)

    unmatched = [_norm(p["email"]) for p in people if _norm(p["email"]) not in assigned]
    return result_pairs, unmatched
