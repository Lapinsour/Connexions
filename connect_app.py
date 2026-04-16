import streamlit as st
import random
from generator import generate_puzzle
from validator import check_group

# init session
if "puzzle" not in st.session_state:
    st.session_state.puzzle = generate_puzzle()

if "selected" not in st.session_state:
    st.session_state.selected = []

puzzle = st.session_state.puzzle

st.title("Connections FR")

# 🎯 grille 4x4
cols = st.columns(4)

for i, word in enumerate(puzzle["words"]):
    col = cols[i % 4]

    if col.button(word, key=word):
        if word in st.session_state.selected:
            st.session_state.selected.remove(word)
        else:
            if len(st.session_state.selected) < 4:
                st.session_state.selected.append(word)

# affichage sélection
st.write("### Sélection :")
st.write(st.session_state.selected)

# validation
if st.button("Valider"):
    if len(st.session_state.selected) != 4:
        st.warning("Sélectionne exactement 4 mots")
    else:
        result = check_group(st.session_state.selected, puzzle)

        if result["correct"]:
            st.success(f"Correct ✅ : {result['category']}")
            st.session_state.selected = []
        else:
            st.error("Incorrect ❌")

# reset puzzle
if st.button("Nouveau puzzle"):
    st.session_state.puzzle = generate_puzzle()
    st.session_state.selected = []