import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from datetime import timedelta

# Google Sheets-пен байланыс орнату
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Sheets файл атауы және парағы
SHEET_NAME = "Booking_kuiz_ui"
WORKSHEET_NAME = "kuiz_ui"

sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

def get_availability():
    data = sheet.get_all_records()
    today = datetime.now().date()

    yurt_data = {"Yurt1": [], "Yurt2": []}
    for row in data:
        yurt = row["Yurt"]
        start = datetime.strptime(row["StartDate"], "%Y-%m-%d %H:%M")
        end = datetime.strptime(row["EndDate"], "%Y-%m-%d %H:%M")
        yurt_data[yurt].append((start, end))

    text = ""
    for yurt, bookings in yurt_data.items():
        text += f"🏕 {yurt}:\n"
        for b in sorted(bookings):
            text += f"   {b[0].strftime('%d %b %H:%M')}–{b[1].strftime('%d %b %H:%M')}: ❌\n"
        text += "\n"
    return text
def add_booking(yurt, start, end, name, phone, notes):
    data = sheet.get_all_records()
    next_id = len(data) + 1  # соңғы ID + 1
    new_row = [next_id, yurt, start, end, name, phone, notes]
    sheet.append_row(new_row)
    return True
def delete_booking_by_id(booking_id):
    records = sheet.get_all_records()
    for i, row in enumerate(records):
        if str(row["ID"]) == str(booking_id):
            sheet.delete_rows(i + 2)  # 1-жол — header, +1 индексация
            return True
    return False
def list_bookings():
    data = sheet.get_all_records()
    text = "📋 Барлық броньдар:\n\n"
    for row in data:
        text += (
            f"#{row['ID']} | {row['Yurt']} | "
            f"{row['StartDate']} – {row['EndDate']} | "
            f"{row['ClientName']} | {row['Phone']}\n"
        )
    return text if len(data) > 0 else "Броньдар жоқ." 
def get_next_available():
    data = sheet.get_all_records()
    today = datetime.now().date()
    now = datetime.now()
    # Киіз үйлер бойынша бронь тізімі
    yurt_data = {"Yurt1": [], "Yurt2": []}
    for row in data:
        yurt = row["Yurt"]
        start = datetime.strptime(row["StartDate"], "%Y-%m-%d %H:%M")
        end = datetime.strptime(row["EndDate"], "%Y-%m-%d %H:%M")
        yurt_data[yurt].append((start, end))

    result = "📅 Келесі бос уақыттар:\n"
    for yurt, bookings in yurt_data.items():
        # броньдарды реттеу
        bookings.sort()
        current_date = now
        for start, end in bookings:
            if current_date >= start and current_date <= end:
                current_date = end + timedelta(days=1)
        result += f"🏕 {yurt} – {current_date.strftime('%Y-%m-%d %H:%M')} бастап бос\n"

    return result
def edit_booking(booking_id, field, new_value):
    data = sheet.get_all_records()
    headers = sheet.row_values(1)

    for i, row in enumerate(data):
        if str(row["ID"]) == str(booking_id):
            col_index = headers.index(field) + 1  # +1 because sheet is 1-indexed
            sheet.update_cell(i + 2, col_index, new_value)  # +2: header + 1-indexing
            return True
    return False