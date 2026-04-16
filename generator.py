import random
from categories import CATEGORIES
import json
from datetime import date

def generate_puzzle():

    selected_cats = random.sample(CATEGORIES, 4)

    groups = []
    words = []

    # 1️⃣ construire les groupes COMPLETS d'abord
    for cat in selected_cats:
        if len(cat["words"]) < 4:
            raise ValueError(f"Catégorie trop petite: {cat['name']}")

        chosen = random.sample(cat["words"], 4)

        groups.append({
            "category": cat["name"],
            "words": chosen
        })

        words.extend(chosen)

    # 2️⃣ NE PAS casser les groupes ici
    # (option : ajouter des leurres SANS remplacement)

    all_decoys = []
    for cat in selected_cats:
        all_decoys.extend(cat.get("decoys", []))

    # injecter des leurres en AJOUT, pas remplacement
    for _ in range(4):  # 4 leurres max
        if all_decoys:
            words[random.randint(0, len(words)-1)] = random.choice(all_decoys)

    random.shuffle(words)

    puzzle = {
        "date": str(date.today()),
        "words": words,
        "groups": groups
    }

    # save
    try:
        with open("puzzles.json", "r", encoding="utf-8") as f:
            puzzles = json.load(f)
    except:
        puzzles = []

    puzzles.append(puzzle)

    with open("puzzles.json", "w", encoding="utf-8") as f:
        json.dump(puzzles, f, indent=2, ensure_ascii=False)

    return puzzle
