import gspread
import pandas as pd
import json
import tempfile
from google.oauth2.service_account import Credentials


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# -------------------------------
# Fungsi untuk koneksi ke Google Sheet (pakai kredensial dict dari st.secrets)
# -------------------------------
def connect_gsheet(creds_dict, sheet_name: str):
    creds_dict = dict(creds_dict)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

# -------------------------------
# Fungsi untuk mengambil data dari Sheet sebagai DataFrame
# -------------------------------
def get_data(sheet):
    records = sheet.get_all_records()
    if records:
        df = pd.DataFrame(records)
    else:
        df = pd.DataFrame(columns=["Tanggal", "Jam Belajar", "Jam Tidur", "Jam Organisasi", "Mood"])
    return df

# -------------------------------
# Fungsi untuk menambahkan data baru
# -------------------------------
def append_data(sheet, row_data):
    sheet.append_row(row_data)
