import streamlit as st 
from PIL import Image #import gambar
from PIL import ImageEnhance
import numpy as np 
import base64
from io import BytesIO

# Fungsi untuk mendownload gambar stego ke dalam bentuk 'PNG'
def get_image_download_link(img, filename, text):
    buffered = BytesIO()
    img.save(buffered, format='png', dpi=(300, 300))
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Fungsi untuk menyesuaikan ukuran cover dengan ukuran message
def resize_image(cover, message):
    return cover.resize(message.size)

# Fungsi untuk menghitung bit sebelum dikonversi ke Numpy Array
def calculate_image_bits_pil(image):
    # Dapatkan ukuran gambar (lebar & tinggi)
    width, height = image.size
    # Kalkulasi jumlah pixel
    num_pixels = width * height
    # Dapatkan mode gambar untuk menentukan jumlah channel.
    mode_to_bits = {
        '1': 1,    # 1-bit piksel, hitam dan putih, disimpan dengan satu piksel per byte
        'L': 8,    # 8-bit piksel, hitam dan putih
        'P': 8,    # 8-bit piksel, dipetakan ke mode lain menggunakan palet warna
        'RGB': 24, # 3x8-bit piksel, warna asli
        'RGBA': 32,# 4x8-bit piksel, warna asli dengan masker transparansi
        'CMYK': 32,# 4x8-bit piksel, pemisahan warna
        'YCbCr': 24,# 3x8-bit piksel, format video warna
        'LAB': 24, # 3x8-bit piksel, ruang warna Lab
        'HSV': 24, # 3x8-bit piksel, ruang warna Hue, Saturation, Value
        'I': 32,   # 32-bit piksel bilangan bulat bertanda
        'F': 32    # 32-bit piksel titik mengambang
    }
    # Default ke 8 bit jika mode tidak ada dalam library.
    bits_per_pixel = mode_to_bits.get(image.mode, 8) 
    # Hitung jumlah total bit.
    total_bits = num_pixels * bits_per_pixel
    return total_bits

#Fungsi untuk menghitung bit gambar
def calculate_image_bits(image_array):
    dtype = image_array.dtype
    bits_per_element = np.dtype(dtype).itemsize * 8
    total_elements = image_array.size
    total_bits = total_elements * bits_per_element
    return total_bits

# Fungsi enkripsi gambar
def encryptPage():
    # Unggah gambar cover
    st.markdown("<h4 style='text-align: left;'>Unggah Wadah Sampul</h4>", unsafe_allow_html=True)
    cover_file = st.file_uploader('', type=['jpg'], key="cover")
    if cover_file is not None:
        cover = Image.open(cover_file)

        # Unggah gambar pesan
        st.markdown("<h4 style='text-align: left;'>Unggah Sampul Buku</h4>", unsafe_allow_html=True)
        message_file = st.file_uploader('', type=['png','jpg'], key="message")
        if message_file is not None:
            message = Image.open(message_file)

            # Mengecek apakah gambar dalam format CMYK atau RGB
            if message.mode == 'CMYK':
                # Mengonversi ke RGB jika gambar dalam format CMYK
                message = message.convert('RGB')
            
            # Menyamakan ukuran gambar cover dengan gambar pesan
            cover_res = resize_image(cover, message)

            # Ubah ke array untuk manipulasi
            cover_res = np.array(cover_res, dtype=np.uint8)
            message = np.array(message, dtype=np.uint8)

            # "Imbed" adalah jumlah bit dari gambar pesan yang akan disematkan dalam gambar sampul
            imbed = 4

            # Menggeser gambar pesan sebanyak (8 - imbed) bit ke kanan
            messageshift = np.right_shift(message, 8 - imbed)

            # Menampilkan jumlah bit dalam gambar cover
            total_bits_before_conversion = calculate_image_bits_pil(cover)
            st.write(f"Jumlah bit dalam gambar {total_bits_before_conversion:,} bit")
            st.image(cover, caption='Ini adalah gambar wadah yang mengenkripsi')

            # Menampilkan jumlah bit dalam gambar pesan
            total_bits = calculate_image_bits(message)
            st.write(f"Jumlah bit dalam gambar {total_bits:,} bit")

            # Tampilkan gambar pesan hanya dengan bit yang disematkan di layar
            # Harus digeser dari LSB (bit paling rendah) ke MSB (bit paling tinggi)
            showmess = messageshift << (8-imbed)

            # Tampilkan gambar "showmess".
            st.image(showmess, caption='Ini adalah gambar yang akan dienkripsi')

            # Sekarang, hapus bit signifikan terkecil dari gambar penutup.
            mask = 0xFF << imbed  
            
            # Buat masker dengan bit signifikan terkecil `imbed` sebagai 0.
            coverzero = cover_res & mask

            # Kalkulasi jumlah bit gambar setelah di imbed.
            total_bits_after_imbed = calculate_image_bits(coverzero)
            st.write(f"Jumlah bit dalam gambar enkripsi {total_bits_after_imbed:,} bit")

            # Gabungkan coverzero dan messageshift.
            stego = coverzero | messageshift

            # Tampilkan gambar stego.
            st.image(stego, caption='Ini adalah gambar hasil enkripsi', channels='GRAY')

            # Ubah kembali array stego menjadi gambar
            stego_img = Image.fromarray(stego.astype(np.uint8))

            # Create a download link for the stego image
            download_link = get_image_download_link(stego_img, "stego_image.png", "Unduh gambar enkripsi")
            st.markdown(download_link, unsafe_allow_html=True)