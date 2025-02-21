import streamlit as st
from utils.db_utils import get_moods

st.title("Mood History")

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("Please log in first.")
else:
    username = st.session_state["username"]
    moods = get_moods(username)

    if moods:
        for date, mood in moods:
            st.write(f"{date}: {mood}")
    else:
        st.write("No mood history found.")
