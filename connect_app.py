import streamlit as st
from generator import generate_puzzle
from validator import check_group

st.set_page_config(layout="centered")

# CSS grille
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    height: 70px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# INIT STATE
if "puzzle" not in st.session_state:
    st.session_state.puzzle = generate_puzzle()

if "selected" not in st.session_state:
    st.session_state.selected = []

if "found_groups" not in st.session_state:
    st.session_state.found_groups = []


puzzle = st.session_state.puzzle

# 🧠 mots déjà validés
locked_words = set(
    word
    for group in st.session_state.found_groups
    for word in group["words"]
)

st.title("Connections FR")

# 🔲 GRID
cols = st.columns(4)

for i, word in enumerate(puzzle["words"]):
    col = cols[i % 4]
    key = f"w_{i}"

    # ❌ mot déjà trouvé → désactivé
    if word in locked_words:
        col.button(f"✔ {word}", key=key, disabled=True)
        continue

    # 🟨 sélection
    label = f"🟨 {word}" if word in st.session_state.selected else word

    if col.button(label, key=key):
        if word in st.session_state.selected:
            st.session_state.selected.remove(word)
        else:
            if len(st.session_state.selected) < 4:
                st.session_state.selected.append(word)


# 📊 sélection
st.write("### Sélection")
st.write(st.session_state.selected)


# ✅ validation
if st.button("Valider"):
    if len(st.session_state.selected) != 4:
        st.warning("Sélectionne 4 mots")
    else:
        result = check_group(st.session_state.selected, puzzle)

        if result["correct"]:
            st.success(f"✔ Groupe trouvé : {result['category']}")

            # 🔒 verrouiller le groupe
            st.session_state.found_groups.append({
                "category": result["category"],
                "words": st.session_state.selected.copy()
            })

            # reset sélection
            st.session_state.selected = []

        else:
            st.error("❌ Mauvais groupe")


# 🔄 nouveau puzzle
if st.button("Nouveau puzzle"):
    st.session_state.puzzle = generate_puzzle()
    st.session_state.selected = []
    st.session_state.found_groups = []
