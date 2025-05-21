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

recommendations = {
    "grypa": "Udaj się do lekarza i zażyj leki przeciwgorączkowe",
    "przeziębienie": "Odpocznij i okryj się kocem",
    "odra": "Natychmiast skonsultuj się z lekarzem - choroba zakaźna",
    "zapalenie opon mózgowych": "Natychmiast wezwij pogotowie!",
    "alergia": "Zażyj lek przeciwhistaminowy",
    "grypa żołądkowa": "Pij dużo płynów i stosuj dietę lekkostrawną",
    "zawał serca": "Natychmiast wezwij pogotowie!",
    "covid-19": "Zgłoś się na test i zostań w izolacji",
    "infekcja wirusowa": "Odpocznij i pij dużo płynów",
    "reakcja alergiczna": "Zażyj lek przeciwalergiczny i skonsultuj się z lekarzem"
}


def forward_chaining(rules, facts):
    inferred = set(facts)
    recommendations_found = set()
    changed = True
    while changed:
        changed = False
        for premises, conclusion in rules:
            if all(p in inferred for p in premises) and conclusion not in inferred:
                inferred.add(conclusion)
                changed = True
                # Sprawdzamy czy nowy wniosek ma zalecenie
                if conclusion in recommendations:
                    recommendations_found.add(recommendations[conclusion])

    return inferred, recommendations_found


def backward_chaining(rules, goal, facts, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    if goal in facts:
        return True, path

    if goal in visited:
        return False, path
    visited.add(goal)

    for premises, conclusion in rules:
        if conclusion == goal:
            all_premises_true = True
            for p in premises:
                success, subpath = backward_chaining(rules, p, facts, visited, path)
                path.extend(subpath)
                if not success:
                    all_premises_true = False
                    path.append(f"Premisa '{p}' nie jest spelniona")
                    break

            if all_premises_true:
                path.append(f"Wszystkie premisy spełnione - wnioskujemy '{conclusion}'")
                return True, path

    path.append(f"Nie znaleziono regul prowadzacych do '{goal}'")
    return False, path


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
    facts = {"ból mięśni", "kaszel", "utrata węchu", "ból głowy", "ból gardła"}

    print("=== Wnioskowanie w przod ===")
    inferred_diseases, recs = forward_chaining(rules, facts)
    print("\nWszystkie wnioskowane stany:", inferred_diseases)
    if recs:
        print("\nZnalezione zalecenia:")
        for rec in recs:
            print("-", rec)

    print("\n=== Wnioskowanie wstecz ===")
    success, path = backward_chaining(rules, "przeziebienie", facts)
    print("\n".join(path))
    print("\nCzy mogę byc chory na przeziebienie?", "Tak" if success else "Nie")

    print("\n=== Najlepsze dopasowanie choroby ===")
    diagnosis = best_matching_disease(rules, facts)
    if diagnosis:
        disease, matched, total = diagnosis
        print(f"\nNajbardziej prawdopodobna choroba: {disease} ({matched}/{total} objawow)")
        if disease in recommendations:
            print(f"Zalecenie: {recommendations[disease]}")
    else:
        print("Nie można wnioskowac zadnej choroby.")