import streamlit as st

st.title("Pac-Man AI Game")

# --- Shared state (replace with a database in production) ---
if "groups" not in st.session_state:
    # Each group has slots: {"pacman": None, "ghost": None}
    st.session_state.groups = {i: {"pacman": None, "ghost": None} for i in range(1, 21)}

# --- User input ---
group_choice = st.selectbox("Choose your group (1–20)", list(st.session_state.groups.keys()))
role_choice = st.radio("Choose your role", ["Pac-Man", "Ghost"])
username = st.text_input("Enter your name")

# --- Join logic ---
if st.button("Join Game"):
    group = st.session_state.groups[group_choice]
    if role_choice == "Pac-Man":
        if group["pacman"] is None:
            group["pacman"] = username
            st.success(f"You joined Group {group_choice} as Pac-Man 👾")
        else:
            st.error("Pac-Man slot already taken in this group.")
    else:  # Ghost
        if group["ghost"] is None:
            group["ghost"] = username
            st.success(f"You joined Group {group_choice} as Ghost 👻")
        else:
            st.error("Ghost slot already taken in this group.")

# --- Check if group is full ---
group = st.session_state.groups[group_choice]
if group["pacman"] and group["ghost"]:
    st.info(f"Group {group_choice} is ready: Pac-Man = {group['pacman']}, Ghost = {group['ghost']}")
    # Load the HTML game only when both roles are filled
    html_code = open("pacman.html", "r").read()
    st.components.v1.html(html_code, height=600, scrolling=True)
