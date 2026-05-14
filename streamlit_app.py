import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

st.title("Pac-Man AI Game")

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["firebase"].to_dict())  # convert section to dict
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://pacman-ai-eaf08-default-rtdb.asia-southeast1.firebasedatabase.app'
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
        if group_data.get("ghost") is None:
            group_ref.update({"ghost": username})
            st.success("You joined as Ghost")
        else:
            st.error("Ghost slot already taken")

    # Reload group data
    group_data = group_ref.get()
    if group_data.get("pacman") and group_data.get("ghost"):
        st.info("Group ready! Countdown starting...")
    
        countdown_placeholder = st.empty()
        for i in range(3, 0, -1):
            countdown_placeholder.markdown(
                f"""
                <div style="
                    position: relative;
                    height: 600px;
                    background-color: rgba(0,0,0,0.5);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <span style="font-size:100px; color:white;">{i}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            import time
            time.sleep(1)
    
        countdown_placeholder.empty()  # clear overlay
    
        # Load the game after countdown
        html_code = open("pacman.html", "r").read()
        st.components.v1.html(html_code, height=600, scrolling=True)
