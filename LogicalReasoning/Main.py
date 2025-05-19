rules = [
    (["gorączka", "kaszel", "zmęczenie"], "grypa"),
    (["gorączka", "wysypka", "zaczerwienione oczy"], "odra"),
    (["ból głowy", "nudności", "sztywność karku"], "zapalenie opon mózgowych"),
    (["ból gardła", "kaszel", "ból głowy"], "przeziębienie"),
    (["katar", "kichanie", "łzawienie oczu"], "alergia"),
    (["ból brzucha", "nudności", "biegunka"], "grypa żołądkowa"),
    (["ból w klatce piersiowej", "duszność", "zimne poty"], "zawał serca"),
    (["suchy kaszel", "gorączka", "utrata węchu"], "covid-19"),
    (["ból mięśni", "dreszcze", "gorączka"], "infekcja wirusowa"),
    (["wysypka", "swędzenie", "obrzęk"], "reakcja alergiczna")
]

def forward_chaining(rules, facts):
    inferred = set(facts)
    changed = True
    while changed:
        changed = False
        for premises, conclusion in rules:
            if all(p in inferred for p in premises) and conclusion not in inferred:
                inferred.add(conclusion)
                changed = True
    return inferred

def backward_chaining(rules, goal, facts, visited=None):
    if visited is None:
        visited = set()

    if goal in facts:
        return True

    if goal in visited:
        return False
    visited.add(goal)

    for premises, conclusion in rules:
        if conclusion == goal:
            print(f"Sprawdzam regułę: {premises} → {conclusion}")
            if all(backward_chaining(rules, p, facts, visited) for p in premises):
                return True, goal
    return False, None

def best_matching_disease(rules, facts):
    best_match = None
    best_score = 0
    for premises, disease in rules:
        score = sum(1 for p in premises if p in facts)
        if score > best_score:
            best_score = score
            best_match = (disease, score, len(premises))
    return best_match

if __name__ == "__main__":
    facts = {"ból mięśni", "kaszel", "utrata węchu", "ból głowy", "ból gardła", "kaszel", "ból głowy"}

    inferred = forward_chaining(rules, facts)
    print("\nWszystkie wnioskowane stany:", inferred)

    result, disease = backward_chaining(rules, "przeziębienie", facts)
    print("\nCzy mogę być chory na", disease, "?", "Tak" if result else "Nie")

    diagnosis = best_matching_disease(rules, facts)
    if diagnosis:
        disease, matched, total = diagnosis
        print(f"\nNajbardziej prawdopodobna choroba: {disease} ({matched}/{total} objawów)")
    else:
        print("Nie można wnioskować żadnej choroby.")