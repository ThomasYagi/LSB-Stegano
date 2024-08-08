import streamlit as st 
from PIL import Image
import numpy as np
from decrypt import decryptPage
from encrypt import encryptPage
from database import init_db, add_user, get_user

st.set_page_config(page_title="LSB Stego App", page_icon=":eyes:", layout="wide")

# Initialize the database
init_db()

# User management functions
def register_user(username, password):
    success = add_user(username, password)
    if success:
        return True, "Registration successful"
    else:
        return False, "Username already exists"

def login_user(username, password):
    user = get_user(username)
    if user and user[0] == password:
        return True, "Login successful"
    return False, "Invalid credentials"

# Check URL parameters to update session state
query_params = st.experimental_get_query_params()
if "logged_in" in query_params and query_params["logged_in"][0] == "true":
    st.session_state["logged_in"] = True
    st.session_state["username"] = query_params["username"][0]

# Login and Register pages
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
                st.experimental_set_query_params(logged_in="true", username=username)
            else:
                st.error(message)

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
                st.experimental_set_query_params(logged_in="true", username=username)
            else:
                st.error(message)

# Set up the Streamlit app
def main_app():
    st.title('Tugas Akhir')
    st.header('Steganografi LSB pada Sampul Buku')

    st.write("---")

    PAGES = {
        "Enkripsi" : encryptPage,
        "Dekripsi": decryptPage,
    }

    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Pilih menu", list(PAGES.keys()))

    page = PAGES[selection]
    page()

# Navigation
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    main_app()
else:
    page = st.sidebar.selectbox("Pilih Halaman", ["Login", "Register"])
    if page == "Login":
        login_page()
    else:
        register_page()