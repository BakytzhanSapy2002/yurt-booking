# backend/update_calendar_data.py
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def update_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    SHEET_NAME = "Booking_kuiz_ui"
    WORKSHEET_NAME = "calendar_data"
    sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

    # Күндер диапазоны: бүгіннен бастап 30 күн
    today = datetime.now().date()
    last_day = today + timedelta(days=30)

    # Барлық жолдарды оқу
    all_data = sheet.get_all_values()
    headers = all_data[0]
    rows = all_data[1:]

    # Қалыптастыру
    filtered = [row for row in rows if today <= datetime.strptime(row[0], "%Y-%m-%d").date() <= last_day]

    # Sheet тазалау және қайта жазу
    sheet.clear()
    sheet.append_row(headers)
    if filtered:
        sheet.append_rows(filtered)

    print("✅ Тек ағымдағы және алдағы 30 күнге арналған жазбалар сақталды.")
