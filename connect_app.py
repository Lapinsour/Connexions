import streamlit as st
from generator import generate_puzzle
from validator import check_group

GROUP_COLORS = ["#f9d342", "#7bd389", "#6ec1e4", "#c084fc"]

st.set_page_config(layout="centered")

# 🎨 CSS global
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    height: 70px;
    font-size: 16px;
    border-radius: 8px;
    transition: 0.2s;
}
</style>
""", unsafe_allow_html=True)

# 🧠 INIT STATE
if "puzzle" not in st.session_state:
    st.session_state.puzzle = generate_puzzle()

if "selected" not in st.session_state:
    st.session_state.selected = []

if "found_groups" not in st.session_state:
    st.session_state.found_groups = []

puzzle = st.session_state.puzzle

# Vies
if "lives" not in st.session_state:
    st.session_state.lives = 4
if st.session_state.lives <= 0:
    st.title("💀 Partie terminée")
    st.warning("Reviens demain pour un nouveau puzzle !")
    st.stop()
st.write(f"❤️ Vies restantes : {st.session_state.lives}")

# mots déjà trouvés
hidden_words = set(
    w for g in st.session_state.found_groups for w in g["words"]
)


# 🔲 GRID
cols = st.columns(4)

visible_words = [w for w in puzzle["words"] if w not in hidden_words]

for i, word in enumerate(visible_words):

    col = cols[i % 4]
    key = f"word_{word}"

    # 🎨 couleur si sélectionné
    if word in st.session_state.selected:
        label = f"🟨 {word}"
    else:
        label = word

    if col.button(label, key=key):

        # toggle sélection
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

            # 🔥 trouver groupe complet
            group_words = st.session_state.selected.copy()

            st.session_state.found_groups.append({
                "category": result["category"],
                "words": group_words
            })

            st.success(f"✔ {result['category']}")

            # 💥 animation pseudo-disparition (rerun)
            st.session_state.selected = []

        else:
            st.session_state.lives -= 1
            st.error("❌ Mauvais groupe")

if len(st.session_state.found_groups) == 4:
    st.success("🎉 Puzzle terminé !")
