import streamlit as st
from PIL import Image
from PIL import ImageEnhance
import numpy as np
import base64
from io import BytesIO

# Fungsi untuk mendownload gambar stego ke dalam bentuk 'JPG'
def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    if img.mode in ('RGBA', 'P'):  # Jika gambar memiliki alpha channel
        img = img.convert('RGB')  # Konversi ke 'RGB'
    img.save(buffered, format='JPEG')  # Gunakan 'JPEG' sebagai format penyimpanan
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/jpeg;base64,{img_str}" download="{filename}">{text}</a>'  # Use 'image/jpeg' as the MIME type
    return href

# Fungsi untuk menghitung bit sebelum dikonversi ke Numpy Array
def calculate_image_bits_pil(image):
    if isinstance(image, Image.Image):
        width, height = image.size
        mode_to_bits = {
            '1': 1,    # 1-bit pixels, black and white, stored with one pixel per byte
            'L': 8,    # 8-bit pixels, black and white
            'P': 8,    # 8-bit pixels, mapped to any other mode using a color palette
            'RGB': 24, # 3x8-bit pixels, true color
            'RGBA': 32,# 4x8-bit pixels, true color with transparency mask
            'CMYK': 32,# 4x8-bit pixels, color separation
            'YCbCr': 24,# 3x8-bit pixels, color video format
            'LAB': 24, # 3x8-bit pixels, the L*a*b color space
            'HSV': 24, # 3x8-bit pixels, Hue, Saturation, Value color space
            'I': 32,   # 32-bit signed integer pixels
            'F': 32    # 32-bit floating point pixels
        }
        bits_per_pixel = mode_to_bits.get(image.mode, 8) # Default to 8 bits if mode is not in the dictionary
        total_pixels = width * height
        total_bits = total_pixels * bits_per_pixel
        return total_bits
    else:
        raise TypeError("Expected a PIL Image object, got {}".format(type(image)))

# Fungsi untuk menghitung bit gambar
def calculate_image_bits(image_array):
    dtype = image_array.dtype
    bits_per_element = np.dtype(dtype).itemsize * 8
    total_elements = image_array.size
    total_bits = total_elements * bits_per_element
    return total_bits

# Fungsi dekripsi gambar
def decryptPage():
    st.markdown("<h4 style='text-align: left;'>Unggah Gambar Enkripsi</h4>", unsafe_allow_html=True)
    stego_file = st.file_uploader('', type=['png','jpg'],key="decrypt")
    if stego_file is not None:
        stego = Image.open(stego_file)

        # Ubah menjadi double untuk manipulasi
        stego = np.array(stego, dtype=np.uint8)

        # Inisialisasi pesan yang diekstrak
        extracted_message = np.zeros(stego.shape, dtype=np.uint8)

        # "Imbed" adalah jumlah bit dari gambar pesan yang akan disematkan dalam gambar sampul
        imbed = 4

        # Ekstrak bit paling tidak signifikan (LSB) dari gambar stego
        for i in range(imbed):
            extracted_message = extracted_message | ((stego & (1 << i)) << (8 - imbed))

        extracted_message_img = Image.fromarray(extracted_message.astype('uint8'), 'RGB')

        # Menampilkan jumlah bit dalam gambar pesan
        total_bits_extracted_after = calculate_image_bits(extracted_message)
        st.write(f"Jumlah bit dalam gambar yang diekstrak setelah konversi: {total_bits_extracted_after:,} bit")

        # Tampilkan gambar akhir
        st.image(extracted_message_img, caption='Ini adalah gambar terenkripsi')

        # Tambahkan link download
        st.markdown(get_image_download_link(extracted_message_img, 'result.jpg', 'Download gambar sampul'), unsafe_allow_html=True)