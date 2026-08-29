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


def _shared_interest(p1: dict, p2: dict) -> int:
    score = 0
    if _norm(p1.get("drink")) and _norm(p1.get("drink")) == _norm(p2.get("drink")):
        score += 1
    if _norm(p1.get("want_to_learn")) and _norm(p1.get("want_to_learn")) == _norm(
        p2.get("want_to_learn")
    ):
        score += 1
    return score


def run_matching(
    opted_in_people: list[dict], existing_matches: list[dict]
) -> tuple[list[tuple[str, str]], list[str]]:
    """Greedily pair opted-in people, prioritizing shared drink/want_to_learn,
    excluding repeat matches and same-country/same-section pairs.
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
            country1, country2 = _norm(p1.get("country")), _norm(p2.get("country"))
            if country1 and country1 == country2:
                continue
            section1, section2 = _norm(p1.get("section")), _norm(p2.get("section"))
            if section1 and section1 == section2:
                continue
            score = _shared_interest(p1, p2)
            candidate_pairs.append((score, e1, e2))

    candidate_pairs.sort(key=lambda x: x[0], reverse=True)

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
