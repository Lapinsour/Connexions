import streamlit as st
from generator import generate_puzzle
from validator import check_group

st.set_page_config(layout="centered")

# 🎨 CSS grille
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    height: 70px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# 🧠 session state
if "puzzle" not in st.session_state:
    st.session_state.puzzle = generate_puzzle()

if "selected" not in st.session_state:
    st.session_state.selected = []

puzzle = st.session_state.puzzle

st.title("Connections FR")

# 🔲 grille 4x4
cols = st.columns(4)

for i, word in enumerate(puzzle["words"]):
    col = cols[i % 4]
    key = f"w_{i}"

    label = f"🟨 {word}" if word in st.session_state.selected else word

    if col.button(label, key=key):
        if word in st.session_state.selected:
            st.session_state.selected.remove(word)
        else:
            if len(st.session_state.selected) < 4:
                st.session_state.selected.append(word)

# 📊 affichage sélection
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
            st.session_state.selected = []
        else:
            st.error("❌ Mauvais groupe")

# 🔄 nouveau puzzle
if st.button("Nouveau puzzle"):
    st.session_state.puzzle = generate_puzzle()
    st.session_state.selected = []
