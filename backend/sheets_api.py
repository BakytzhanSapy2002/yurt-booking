import json
import os
import gspread
from google.oauth2.service_account import Credentials

# ✅ Render-дегі environment ішінен Google Service Account JSON-ды алу
GOOGLE_CREDENTIALS_JSON = os.environ.get("GOOGLE_CREDENTIALS_JSON")

if not GOOGLE_CREDENTIALS_JSON:
    raise Exception("GOOGLE_CREDENTIALS_JSON environment variable not set!")

# ✅ Google Sheets API-ге қосылу
creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
client = gspread.authorize(creds)
# print(creds.service_account_email)

# 🗂️ Sheet және Worksheet
SPREADSHEET_NAME = "Booking_kuiz_ui"     # Sheets атауы
WORKSHEET_NAME = "calendar_data"            # Worksheet атауы
sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)

# ✅ Барлық деректерді алу
def get_calendar_data():
    return sheet.get_all_records()

# ✅ Бронь жаңарту функциясы
def update_booking_status(date, obj_type, size, number, status, client="", phone="", notes=""):
    data = sheet.get_all_records()
    headers = sheet.row_values(1)

    for idx, row in enumerate(data):
        if (row["Date"] == date and row["Type"] == obj_type and
            str(row["Size"]) == str(size) and str(row["Number"]) == str(number)):

            row_number = idx + 2  # 1-based indexing

            updates = {
                "Status": status,
                "ClientName": client,
                "Phone": phone,
                "Notes": notes,
            }

            for col_name, value in updates.items():
                if col_name in headers:
                    col_index = headers.index(col_name) + 1
                    sheet.update_cell(row_number, col_index, value)

            return True

    return False

# ✅ Альтернативті атпен екінші функция
def update_status(date, obj_type, size, number, new_status, client="", phone="", notes=""):
    return update_booking_status(date, obj_type, size, number, new_status, client, phone, notes)
