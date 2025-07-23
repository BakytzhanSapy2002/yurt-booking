from datetime import datetime, timedelta
import gspread
import os
import json
from google.oauth2.service_account import Credentials

def generate_free_rows(date_str):
    """Берілген күнге арналған бос броньдар тізімі"""
    rows = []
    for type_ in ["Tapchan", "Yurt"]:
        for size in ["Small", "Large"]:
            price = 8000 if size == "Small" and type_ == "Tapchan" else (
                    15000 if size == "Large" and type_ == "Tapchan" else (
                    20000 if size == "Small" and type_ == "Yurt" else 40000))
            room_count = 10 if type_ == "Tapchan" else 2
            for i in range(1, room_count + 1):
                rows.append([date_str, type_, size, str(i), str(price), "free"])
    return rows

def update_sheet():
    # ✅ Авторизация Google Sheets API
    GOOGLE_CREDENTIALS_JSON = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if not GOOGLE_CREDENTIALS_JSON:
        raise Exception("GOOGLE_CREDENTIALS_JSON environment variable not set!")

    creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)

    # 🗂️ Sheet және Worksheet атауы
    SHEET_NAME = "Booking_kuiz_ui"
    WORKSHEET_NAME = "calendar_data"
    sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

    # 📅 Бүгіннен бастап 30 күнге дейінгі аралық
    today = datetime.today().date()
    last_day = today + timedelta(days=30)

    all_data = sheet.get_all_values()
    headers = all_data[0]
    rows = all_data[1:]

    existing_dates = set()
    for row in rows:
        try:
            row_date = datetime.strptime(row[0].strip(), "%Y-%m-%d").date()
            if today <= row_date <= last_day:
                existing_dates.add(row_date)
        except Exception:
            continue

    new_rows = []
    for delta in range((last_day - today).days + 1):
        day = today + timedelta(days=delta)
        if day not in existing_dates:
            new_rows.extend(generate_free_rows(day.strftime("%Y-%m-%d")))

    filtered_rows = [row for row in rows if today <= datetime.strptime(row[0].strip(), "%Y-%m-%d").date() <= last_day]
    sheet.clear()
    sheet.append_row(headers)

    if filtered_rows:
        sheet.append_rows(filtered_rows)
    if new_rows:
        sheet.append_rows(new_rows)

    print(f"✅ Барлығы {len(filtered_rows)} бұрынғы + {len(new_rows)} жаңа бос орындар жазылды.")

# Егер local режимде тест керек болса:
# update_sheet()
