import random
import json
from datetime import date
from categories import CATEGORIES


def generate_puzzle():

    # 1️⃣ vérifier intégrité dataset
    for cat in CATEGORIES:
        if len(cat["words"]) != 4:
            raise ValueError(f"Catégorie invalide (pas 4 mots): {cat['name']}")

    # 2️⃣ choisir 4 catégories
    selected = random.sample(CATEGORIES, 4)

    groups = []
    words = []

    # 3️⃣ construire puzzle proprement
    for cat in selected:
        groups.append({
            "category": cat["name"],
            "words": cat["words"].copy()
        })
        words.extend(cat["words"])

    # 4️⃣ shuffle final uniquement
    random.shuffle(words)

    puzzle = {
        "date": str(date.today()),
        "words": words,
        "groups": groups
    }

    # 5️⃣ sauvegarde optionnelle
    try:
        with open("puzzles.json", "r", encoding="utf-8") as f:
            puzzles = json.load(f)
    except:
        puzzles = []

    puzzles.append(puzzle)

    with open("puzzles.json", "w", encoding="utf-8") as f:
        json.dump(puzzles, f, indent=2, ensure_ascii=False)

    return puzzle


if __name__ == "__main__":
    print(generate_puzzle())
