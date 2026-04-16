def check_group(selected_words, puzzle):
    """
    selected_words : liste de 4 mots sélectionnés
    puzzle : dictionnaire retourné par generator.py
    Retourne :
        {correct: bool, category: str ou None}
    """
    selected_set = set(selected_words)

    for group in puzzle["groups"]:
        group_set = set(group["words"])
        if selected_set == group_set:
            return {"correct": True, "category": group["category"]}

    return {"correct": False, "category": None}


# Test rapide
if __name__ == "__main__":
    from generator import generate_puzzle
    puzzle = generate_puzzle()
    print("Grille :", puzzle["words"])
    # Exemple de test
    test = puzzle["groups"][0]["words"]
    result = check_group(test, puzzle)
    print("Test validation :", result)