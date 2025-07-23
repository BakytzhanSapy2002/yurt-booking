import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# Авторизация
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Sheet таңдау
SHEET_NAME = "Booking_kuiz_ui"
WORKSHEET_NAME = "calendar_data"
sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# Тазалау және тақырып жолы
sheet.clear()
sheet.append_row(["Date", "Type", "Size", "Number", "Price", "Status", "ClientName", "Phone", "Notes"])

# Объект түрлері
object_types = [
    {"type": "Tapchan", "size": "Small", "price": 8000, "count": 10},
    {"type": "Tapchan", "size": "Large", "price": 15000, "count": 10},
    {"type": "Yurt", "size": "Small", "price": 25000, "count": 2},
    {"type": "Yurt", "size": "Large", "price": 40000, "count": 2},
]

# Күндер аралығы
start_date = datetime(2025, 7, 22 )
end_date = datetime(2025, 8, 13)

rows = []

while start_date <= end_date:
    date_str = start_date.strftime("%Y-%m-%d")

    for obj in object_types:
        for i in range(1, obj["count"] + 1):
            rows.append([
                date_str,
                obj["type"],
                obj["size"],
                i,
                obj["price"],
                "free",
                "", "", ""
            ])
    start_date += timedelta(days=1)

# Sheets-ке қосу
sheet.append_rows(rows)
print("✅ Барлық күндер мен объектілер енгізілді.")
