import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# Scope akses untuk Google Sheets dan Google Drive
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# -------------------------------
# Fungsi untuk koneksi ke Google Sheet
# -------------------------------
def connect_gsheet(json_keyfile: str, sheet_name: str):
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1  # akses worksheet pertama
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
