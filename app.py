import streamlit as st 
from PIL import Image
import numpy as np
import time
from decrypt import decryptPage
from encrypt import encryptPage
from database import add_user, get_user

st.set_page_config(page_title="LSB Stego App", page_icon=":eyes:", layout="wide")

# Initialize session state for user authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = get_user(username)
        if user and user[1] == password:
            st.session_state.logged_in = True
            st.success("Login successful")
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def register():
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if get_user(username):
            st.error("Username already exists")
        else:
            add_user(username, password)
            st.success("Registration successful")

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

if st.session_state.logged_in:
    main_app()
else:
    st.sidebar.title("Authentication")
    auth_action = st.sidebar.radio("Login/ Register", ["Login", "Register"])
    if auth_action == "Login":
        login()
    else:
        register()