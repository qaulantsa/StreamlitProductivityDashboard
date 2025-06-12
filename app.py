# =======================
# IMPORT LIBRARY UTAMA
# =======================
import streamlit as st                # Untuk membuat UI aplikasi web interaktif
import pandas as pd                  # Untuk manipulasi data tabular (DataFrame)
import sys                           # Untuk memodifikasi path import module
import os                            # Untuk mengelola path file dan direktori

# =======================
# SET PATH MODULE UTILS
# =======================
# Tambahkan folder 'utils' ke sistem path agar modul dalam folder tersebut bisa diimpor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils')))

# Import fungsi koneksi dan manipulasi data Google Sheet dari file google_sheet.py di folder utils
from utils.google_sheet import connect_gsheet, get_data, append_data

# =======================
# KONFIGURASI APLIKASI
# =======================
# Atur konfigurasi halaman Streamlit
st.set_page_config(page_title="Dashboard Produktivitas Mahasiswa", layout="centered")
st.title("📊 Dashboard Produktivitas Mahasiswa")

# =======================
# KONEKSI GOOGLE SHEET
# =======================
# Hubungkan ke Google Sheet dengan file kredensial dan nama spreadsheet
sheet = connect_gsheet("cred.json", "DashboardProduktivitas")

# =======================
# AMBIL DATA DARI GOOGLE SHEET
# =======================
df = get_data(sheet)           # Ambil data dan simpan dalam DataFrame
df.columns = df.columns.str.strip()  # Bersihkan spasi di nama kolom (antisipasi error)

# Debugging: tampilkan nama kolom yang terbaca dari Google Sheet
st.write("Kolom-kolom yang terbaca:", df.columns.tolist())

# =======================
# TAMPILKAN DATA AKTIVITAS
# =======================
st.subheader("📋 Data Aktivitas Mahasiswa")
st.dataframe(df)   # Tampilkan isi data dalam bentuk tabel

# =======================
# FORM INPUT DATA BARU
# =======================
st.subheader("➕ Tambahkan Data Baru")

# Form input untuk menambahkan data baru
with st.form("data_form", clear_on_submit=True):
    tanggal = st.date_input("Tanggal")                          # Input tanggal
    jam_belajar = st.number_input("Jam Belajar", min_value=0.0, step=0.5)       # Input jam belajar
    jam_tidur = st.number_input("Jam Tidur", min_value=0.0, step=0.5)           # Input jam tidur
    jam_organisasi = st.number_input("Jam Organisasi", min_value=0.0, step=0.5) # Input jam organisasi
    mood = st.selectbox("Mood", ["Sangat Baik", "Baik", "Biasa", "Buruk"])      # Pilih mood
    submitted = st.form_submit_button("Simpan")                # Tombol simpan

    # Jika form disubmit
    if submitted:
        # Buat baris baru sebagai list
        new_row = [str(tanggal), jam_belajar, jam_tidur, jam_organisasi, mood]
        # Tambahkan baris ke Google Sheet
        append_data(sheet, new_row)
        # Tampilkan notifikasi sukses
        st.success("✅ Data berhasil disimpan!")

# =======================
# VISUALISASI DATA
# =======================
st.subheader("📈 Visualisasi Aktivitas")

# Jika DataFrame tidak kosong dan kolom 'Tanggal' tersedia
if not df.empty and "Tanggal" in df.columns:
    # Konversi kolom 'Tanggal' menjadi tipe datetime
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")

    # Hapus baris yang gagal dikonversi (jika ada)
    df = df.dropna(subset=["Tanggal"])

    # Urutkan data berdasarkan tanggal
    df = df.sort_values("Tanggal")

    # Tampilkan grafik garis untuk jam belajar, tidur, dan organisasi
    st.line_chart(df.set_index("Tanggal")[["Jam Belajar", "Jam Tidur", "Jam Organisasi"]])

    # Hitung jumlah kemunculan tiap mood dan tampilkan sebagai bar chart
    mood_count = df["Mood"].value_counts()
    st.bar_chart(mood_count)

# Jika data kosong atau tidak valid
else:
    st.info("Belum ada data yang valid. Silakan tambahkan data terlebih dahulu.")

# =======================
# FOOTER APLIKASI
# =======================
st.markdown("---")
st.caption("Dibuat oleh Qaulan | Tugas Streamlit Dashboard")
