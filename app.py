import streamlit as st
from utils.db_utils import create_user, authenticate_user

# Initialize session state
if "username" not in st.session_state:
    st.session_state.username = None
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def main():
    st.title("Mood Tracker App")

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Register":
        st.subheader("Create a New Account")
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")

        if st.button("Register"):
            success = create_user(new_username, new_password)
            if success:
                st.session_state.username = new_username
                st.session_state.authenticated = True
                st.success("Registration successful! Redirecting to questionnaire...")
                st.switch_page("pages/questionnaire.py")  # ✅ Redirecting only after registration
            else:
                st.error("Username already exists. Try a different one.")

    elif choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state.username = username
                st.session_state.authenticated = True
                st.success("Login successful! Redirecting to dashboard...")
                st.switch_page("pages/dashboard.py")  # ✅ Skip questionnaire for returning users
            else:
                st.error("Invalid credentials, please try again.")

if __name__ == "__main__":
    main()
