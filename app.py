import streamlit as st
import sqlite3
from utils.db_utils import create_user, authenticate_user, save_mood, get_moods
from datetime import datetime

st.title("Mental Health Mood Tracker")

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

# User Authentication
if not st.session_state["logged_in"]:
    choice = st.radio("Login or Register", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Register":
        if st.button("Sign Up"):
            if create_user(username, password):
                st.success("Account created! Please log in.")
            else:
                st.error("User already exists!")

    else:
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Invalid credentials")

# Mood Tracker Section
if st.session_state["logged_in"]:
    st.subheader(f"Hello, {st.session_state['username']}! How are you today?")
    
    today = datetime.today().strftime('%Y-%m-%d')
    mood_options = ["Happy", "Sad", "Stressed", "Anxious", "Calm", "Excited"]
    mood = st.selectbox("Select your mood", mood_options)

    if st.button("Save Mood"):
        save_mood(st.session_state["username"], today, mood)
        st.success("Mood saved!")

    # Show Mood History
    st.subheader("Mood History")
    moods = get_moods(st.session_state["username"])
    if moods:
        for date, mood in moods:
            st.write(f"{date}: {mood}")
    else:
        st.write("No mood records found.")
