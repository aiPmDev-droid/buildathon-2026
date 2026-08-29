import random


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


OVERLAP_FIELDS = ["favorite_spot_la", "excited_about", "biggest_challenge"]


def _has_overlap(p1: dict, p2: dict) -> bool:
    """True if two people share ANY answer verbatim."""
    for field in OVERLAP_FIELDS:
        v1, v2 = _norm(p1.get(field)), _norm(p2.get(field))
        if v1 and v1 == v2:
            return True
    return False


def run_matching(
    opted_in_people: list[dict], existing_matches: list[dict]
) -> tuple[list[tuple[str, str]], list[str]]:
    """Greedily pair opted-in people. A pair is only eligible if they share
    NONE of their answers, aren't from the same city/section, and have never
    been matched before — the app is built to push people outside their
    usual circle, not validate what they already have in common.
    """
    people = [p for p in opted_in_people if p.get("email")]
    random.shuffle(people)  # vary assignment order between runs

    already_matched = _already_matched_pairs(existing_matches)

    candidate_pairs = []
    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            p1, p2 = people[i], people[j]
            e1, e2 = _norm(p1["email"]), _norm(p2["email"])
            if frozenset({e1, e2}) in already_matched:
                continue
            city1, city2 = _norm(p1.get("city")), _norm(p2.get("city"))
            if city1 and city1 == city2:
                continue
            section1, section2 = _norm(p1.get("section")), _norm(p2.get("section"))
            if section1 and section1 == section2:
                continue
            if _has_overlap(p1, p2):
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
