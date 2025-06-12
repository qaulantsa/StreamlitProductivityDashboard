# =======================
# IMPORT LIBRARY UTAMA
# =======================
import streamlit as st
import pandas as pd
import sys
import os

# =======================
# SET PATH MODULE UTILS
# =======================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils')))
from utils.google_sheet import connect_gsheet, get_data, append_data

# =======================
# KONFIGURASI APLIKASI
# =======================
st.set_page_config(page_title="Dashboard Produktivitas Mahasiswa", layout="centered")
st.title("📊 Dashboard Produktivitas Mahasiswa")

# =======================
# KONEKSI GOOGLE SHEET
# =======================
# Ambil kredensial dari secrets dan sambungkan ke Google Sheet
sheet = connect_gsheet(st.secrets["google_service_account"], "DashboardProduktivitas")

# =======================
# AMBIL DATA DARI GOOGLE SHEET
# =======================
df = get_data(sheet)
df.columns = df.columns.str.strip()

# Debugging: tampilkan kolom
st.write("Kolom-kolom yang terbaca:", df.columns.tolist())

# =======================
# TAMPILKAN DATA
# =======================
st.subheader("📋 Data Aktivitas Mahasiswa")
st.dataframe(df)

# =======================
# FORM INPUT DATA BARU
# =======================
st.subheader("➕ Tambahkan Data Baru")

with st.form("data_form", clear_on_submit=True):
    tanggal = st.date_input("Tanggal")
    jam_belajar = st.number_input("Jam Belajar", min_value=0.0, step=0.5)
    jam_tidur = st.number_input("Jam Tidur", min_value=0.0, step=0.5)
    jam_organisasi = st.number_input("Jam Organisasi", min_value=0.0, step=0.5)
    mood = st.selectbox("Mood", ["Sangat Baik", "Baik", "Biasa", "Buruk"])
    submitted = st.form_submit_button("Simpan")

    if submitted:
        new_row = [str(tanggal), jam_belajar, jam_tidur, jam_organisasi, mood]
        append_data(sheet, new_row)
        st.success("✅ Data berhasil disimpan!")

# =======================
# VISUALISASI DATA
# =======================
st.subheader("📈 Visualisasi Aktivitas")

if not df.empty and "Tanggal" in df.columns:
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
    df = df.dropna(subset=["Tanggal"])
    df = df.sort_values("Tanggal")
    st.line_chart(df.set_index("Tanggal")[["Jam Belajar", "Jam Tidur", "Jam Organisasi"]])
    mood_count = df["Mood"].value_counts()
    st.bar_chart(mood_count)
else:
    st.info("Belum ada data yang valid. Silakan tambahkan data terlebih dahulu.")

# =======================
# FOOTER
# =======================
st.markdown("---")
st.caption("Dibuat oleh Qaulan | Tugas Streamlit Dashboard")