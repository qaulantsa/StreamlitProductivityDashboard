import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import json
import tempfile

# Scope akses untuk Google Sheets dan Google Drive
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# -------------------------------
# Fungsi untuk koneksi ke Google Sheet (pakai kredensial dict dari st.secrets)
# -------------------------------
def connect_gsheet(creds_dict: dict, sheet_name: str):
    # Ubah menjadi dict biasa
    creds_dict = dict(creds_dict)

    # Simpan kredensial sementara dalam file temp
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as tmp:
        json.dump(creds_dict, tmp)
        tmp.flush()
        creds = ServiceAccountCredentials.from_json_keyfile_name(tmp.name, scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name).sheet1
    return sheet

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
