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
    st.title("Masuk")
    username = st.text_input("Nama Pengguna")
    password = st.text_input("Kata Sandi", type="password")
    if st.button("Masuk"):
        if not username or not password:
            st.error("Nama pengguna dan kata sandi tidak boleh kosong!")
        else:
            user = get_user(username)
            if user and user[1] == password:
                st.session_state.logged_in = True
                st.success("Pengguna berhasil masuk, tunggu sebentar...")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error("Nama pengguna atau kata sandi salah")

def register():
    st.title("Daftar")
    username = st.text_input("Nama Pengguna")
    password = st.text_input("Kata Sandi", type="password")
    if st.button("Daftar"):
        if get_user(username):
            st.error("Nama pengguna telah digunakan!")
        else:
            add_user(username, password)
            st.success("Pendaftaran pengguna berhasil!")

def main_app():
    st.title('Tugas Akhir')
    st.header('Steganografi LSB pada Sampul Buku')

    st.write("---")

    PAGES = {
        "Enkripsi" : encryptPage,
        "Dekripsi": decryptPage,
    }

    st.sidebar.title("Menu")
    if 'current_page' not in st.session_state:
        st.session_state.current_page = list(PAGES.keys())[0]
    selection = st.sidebar.radio("Pilih menu", list(PAGES.keys()), index=list(PAGES.keys()).index(st.session_state.current_page))

    # Update current_page state
    st.session_state.current_page = selection

    page = PAGES[selection]
    page()

    # Add a logout button in the sidebar
    if st.sidebar.button("Keluar"):
        st.session_state.logged_in = False
        st.experimental_rerun()

if st.session_state.logged_in:
    main_app()
else:
    st.sidebar.title("Autentikasi")
    auth_action = st.sidebar.radio("Pengguna perlu masuk ke dalam sistem terlebih dahulu", ["Masuk", "Daftar"])
    if auth_action == "Masuk":
        login()
    else:
        register()