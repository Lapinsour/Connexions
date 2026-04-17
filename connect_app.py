import streamlit as st
from generator import generate_puzzle
from validator import check_group

GROUP_COLORS = ["#f9d342", "#7bd389", "#6ec1e4", "#c084fc"]

st.set_page_config(layout="centered")

st.markdown("""
<style>

/* empêche le wrap des colonnes */
[data-testid="column"] {
    min-width: 0 !important;
}

/* container des colonnes */
[data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap !important;
}

/* boutons */
div.stButton > button {
    width: 100%;
    height: 70px;
    font-size: 14px;
    padding: 0;
}

/* 📱 MOBILE */
@media (max-width: 600px) {

    /* réduit taille mais garde 4 colonnes */
    div.stButton > button {
        height: 50px;
        font-size: 11px;
    }

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


# mots déjà trouvés
hidden_words = set(
    w for g in st.session_state.found_groups for w in g["words"]
)
st.markdown("<h1 style='text-align: center;'>Connections !</h1>", unsafe_allow_html=True)
st.write(f"❤️ Vies restantes : {st.session_state.lives}")

if "feedback" in st.session_state:

    if st.session_state.get("feedback_type") == "warning":
        st.warning(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)

    del st.session_state.feedback
    del st.session_state.feedback_type

for group in st.session_state.found_groups:
    st.markdown(f"""
<div class="group-container">
    <div class="group-box">
        <div class="group-title">🟩 {group['category']}</div>
        <div>{", ".join(group["words"])}</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.group-box {
    background: #f3f4f6;
    padding: 8px;
    border-radius: 8px;
    margin-bottom: 6px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

def get_one_away_hint(selected_words, puzzle):
    selected = set(selected_words)

    for group in puzzle["groups"]:
        group_set = set(group["words"])

        if len(selected & group_set) == 3:
            return group["category"]

    return None

# 🔲 GRID
cols = st.columns(4)

visible_words = [w for w in puzzle["words"] if w not in hidden_words]

for row in range(4):
    cols = st.columns(4)

    for col_idx in range(4):
        i = row * 4 + col_idx

        if i >= len(visible_words):
            continue

        word = visible_words[i]

        col = cols[col_idx]
        key = f"w_{i}"

        label = f"🟨 {word}" if word in st.session_state.selected else word

        if col.button(label, key=key):

            if word in st.session_state.selected:
                st.session_state.selected.remove(word)
        
            else:
                if len(st.session_state.selected) < 4:
                    st.session_state.selected.append(word)
        
            # 🚀 AUTO-VALIDATION
            if len(st.session_state.selected) == 4:
        
                result = check_group(st.session_state.selected, puzzle)
        
                if result["correct"]:
        
                    st.session_state.found_groups.append({
                        "category": result["category"],
                        "words": st.session_state.selected.copy()
                    })
        
                    st.session_state.selected = []
        
                else:
                    st.session_state.lives -= 1

                    hint = get_one_away_hint(st.session_state.selected, puzzle)
                    
                    if hint:
                        st.session_state.feedback = "💡 Pas loin ! Il te manque un mot..."
                        st.session_state.feedback_type = "warning"
                    else:
                        st.session_state.feedback = "❌ Mauvais groupe"
                        st.session_state.feedback_type = "error"
        
                    st.session_state.selected = []
        
            st.rerun()





if len(st.session_state.found_groups) == 4:
    st.success("🎉 Puzzle terminé !")
