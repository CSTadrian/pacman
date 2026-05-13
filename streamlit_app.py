import streamlit as st

st.title("Pac-Man AI Game")

# Load your HTML code as a string
html_code = open("pacman.html", "r").read()

# Render inside Streamlit
st.components.v1.html(html_code, height=600, scrolling=True)
