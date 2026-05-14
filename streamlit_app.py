import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

st.title("Pac-Man AI Game")

# Initialize Firebase only once
if not firebase_admin._apps:
    # Load your Firebase service account JSON
    cred = credentials.Certificate("firebase-key.json")  # <-- replace with your file path
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://YOUR_PROJECT_ID.firebaseio.com'  # <-- replace with your Firebase DB URL
    })
    
group_choice = st.selectbox("Choose group (1–20)", list(range(1, 21)))
role_choice = st.radio("Choose role", ["Pac-Man", "Ghost"])
username = st.text_input("Enter your name")

if st.button("Join"):
    # Check backend for group status
    group_ref = db.reference(f"groups/{group_choice}")
    group_data = group_ref.get() or {"pacman": None, "ghost": None}

    if role_choice == "Pac-Man":
        if group_data["pacman"] is None:
            group_ref.update({"pacman": username})
            st.success("You joined as Pac-Man")
        else:
            st.error("Pac-Man slot already taken")
    else:
        if group_data["ghost"] is None:
            group_ref.update({"ghost": username})
            st.success("You joined as Ghost")
        else:
            st.error("Ghost slot already taken")

    # Reload group data
    group_data = group_ref.get()
    if group_data["pacman"] and group_data["ghost"]:
        st.info("Group ready! Loading game...")
        html_code = open("pacman.html", "r").read()
        st.components.v1.html(html_code, height=600, scrolling=True)
        
