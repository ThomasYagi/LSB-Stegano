import streamlit as st 
from PIL import Image
import numpy as np
from decrypt import decryptPage
from encrypt import encryptPage
from database import init_db
from login import login_page
from register import register_page

st.set_page_config(page_title="LSB Stego App", page_icon=":eyes:", layout="wide")

# Initialize the database
init_db()

# Ensure session state is initialized
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

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
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["login"])[0]

if st.session_state["logged_in"] and page == "main":
    main_app()
else:
    if page == "register":
        register_page()
    else:
        login_page()