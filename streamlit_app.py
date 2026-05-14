import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import json
import time

st.set_page_config(layout="centered")
st.title("Pac-Man AI Game")

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"].to_dict())
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://pacman-ai-eaf08-default-rtdb.asia-southeast1.firebasedatabase.app'
    })

# UI: choose group, role, username
group_choice = st.selectbox("Choose group (1–20)", list(range(1, 21)))
role_choice = st.radio("Choose role", ["Pac-Man", "Ghost"])
username = st.text_input("Enter your name")

# Claim slot safely using transaction
def claim_slot(group, role, name):
    slot_ref = db.reference(f"groups/{group}/slots/{role.lower()}")
    def txn(current):
        if current is None:
            return name
        return current  # leave unchanged if already taken
    result = slot_ref.transaction(txn)
    return result == name

if st.button("Join"):
    if not username:
        st.error("Please enter your name before joining.")
    else:
        # Ensure group node exists with default keys to avoid KeyError
        group_ref = db.reference(f"groups/{group_choice}/slots")
        group_ref.update({"pacman": None, "ghost": None})
        success = claim_slot(group_choice, role_choice, username)
        if success:
            st.success(f"You joined group {group_choice} as {role_choice}.")
            st.session_state["joined"] = True
            st.session_state["group"] = group_choice
            st.session_state["role"] = role_choice
            st.session_state["username"] = username
        else:
            st.error(f"{role_choice} slot already taken in group {group_choice}.")

# If joined, show the embedded game (the HTML handles Start, countdown, sync)
if st.session_state.get("joined"):
    st.info("Open the game below. Use the Start button inside the game to ready up.")
    # Read the HTML template and inject group/role/username
    with open("pacman.html", "r", encoding="utf-8") as f:
        html_template = f.read()
    # Safely JSON-encode values for embedding into JS
    injected = html_template.replace("{{GROUP_ID}}", str(st.session_state["group"])) \
                            .replace("{{ROLE}}", st.session_state["role"]) \
                            .replace("{{USERNAME}}", st.session_state["username"])
    st.components.v1.html(injected, height=700, scrolling=True)
