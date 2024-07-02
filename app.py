import streamlit as st 
from PIL import Image
import numpy as np
from decrypt import decryptPage
from encrypt import encryptPage

st.set_page_config(page_title="LSB Stego App", page_icon=":eyes:", layout="wide")

# Set up the Streamlit app
st.title('LSB Steganography App')
st.header('Cover and extract your secret message 👀')

st.write("---")

PAGES = {
    "Encrypt" : encryptPage,
    "Decrypt": decryptPage,
}

st.sidebar.title("What You Want to Do?")
selection = st.sidebar.radio("I want to", list(PAGES.keys()))

page = PAGES[selection]
page()