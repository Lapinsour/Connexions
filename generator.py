import random
from data.categories import CATEGORIES
import json
from datetime import date

def generate_puzzle():
    # Tirer 4 catégories aléatoires
    selected_cats = random.sample(CATEGORIES, 4)
    
    words = []
    groups = []

    for cat in selected_cats:
        chosen = random.sample(cat["words"], 4)
        words.extend(chosen)
        groups.append({
            "category": cat["name"],
            "words": chosen
        })

    # Injection de leurres : 1 mot "decoy" par catégorie, aléatoire
    for cat in selected_cats:
        if "decoys" in cat and cat["decoys"]:
            fake_word = random.choice(cat["decoys"])
            replace_index = random.randint(0, len(words)-1)
            words[replace_index] = fake_word

    random.shuffle(words)

    puzzle = {
        "date": str(date.today()),
        "words": words,
        "groups": groups
    }

    # Sauvegarde dans puzzles.json
    try:
        with open("data/puzzles.json") as f:
            puzzles = json.load(f)
    except FileNotFoundError:
        puzzles = []

    puzzles.append(puzzle)

    with open("data/puzzles.json", "w") as f:
        json.dump(puzzles, f, indent=2, ensure_ascii=False)

    return puzzle

# Pour tester
if __name__ == "__main__":
    puzzle = generate_puzzle()
    print("Puzzle généré :")
    print(puzzle)