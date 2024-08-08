# login.py
import streamlit as st
from database import get_user

def login_user(username, password):
    user = get_user(username)
    if user and user[0] == password:
        return True, "Login successful"
    return False, "Invalid credentials"

def login_page():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            success, message = login_user(username, password)
            if success:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success(message)
                st.experimental_set_query_params(page="main")
            else:
                st.error(message)

    if st.button("Register"):
        st.experimental_set_query_params(page="register")

if __name__ == "__main__":
    login_page()