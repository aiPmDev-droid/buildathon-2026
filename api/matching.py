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


def _overlap_count(p1: dict, p2: dict) -> int:
    """How many answers two people happen to share, verbatim. Lower is better —
    the app deliberately pairs people with the LEAST overlap, to push people
    outside their usual circle rather than validate what they already know."""
    count = 0
    for field in OVERLAP_FIELDS:
        v1, v2 = _norm(p1.get(field)), _norm(p2.get(field))
        if v1 and v1 == v2:
            count += 1
    return count


def run_matching(
    opted_in_people: list[dict], existing_matches: list[dict]
) -> tuple[list[tuple[str, str]], list[str]]:
    """Greedily pair opted-in people, prioritizing the LEAST overlap in answers
    (pushes people toward someone outside their usual circle), excluding
    repeat matches and same-city/same-section pairs.
    """
    people = [p for p in opted_in_people if p.get("email")]
    random.shuffle(people)  # vary tie-break order between runs

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
            score = _overlap_count(p1, p2)
            candidate_pairs.append((score, e1, e2))

    candidate_pairs.sort(key=lambda x: x[0])  # ascending: least overlap first

    assigned: set[str] = set()
    result_pairs: list[tuple[str, str]] = []
    for score, e1, e2 in candidate_pairs:
        if e1 in assigned or e2 in assigned:
            continue
        result_pairs.append((e1, e2))
        assigned.add(e1)
        assigned.add(e2)

    unmatched = [_norm(p["email"]) for p in people if _norm(p["email"]) not in assigned]
    return result_pairs, unmatched
