def check_group(selected_words, puzzle):

    selected = set(selected_words)

    for group in puzzle["groups"]:
        if selected == set(group["words"]):
            return {
                "correct": True,
                "category": group["category"]
            }

    return {
        "correct": False,
        "category": None
    }
