# register.py
import streamlit as st
from database import add_user

def register_user(username, password):
    success = add_user(username, password)
    if success:
        return True, "Registration successful"
    else:
        return False, "Username already exists"

def register_page():
    st.title("Register")
    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")
        if submit:
            success, message = register_user(username, password)
            if success:
                st.success(message)
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.experimental_set_query_params(page="main")
            else:
                st.error(message)

    if st.button("Login"):
        st.experimental_set_query_params(page="login")

if __name__ == "__main__":
    register_page()