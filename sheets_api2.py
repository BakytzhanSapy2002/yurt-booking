# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# from datetime import datetime

# # Авторизация
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
# client = gspread.authorize(creds)

# # Sheet таңдау
# SHEET_NAME = "Booking_kuiz_ui"
# WORKSHEET_NAME = "calendar_data"
# sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

# # Барлық деректерді алу (JSON форматта)
# def get_calendar_data():
#     records = sheet.get_all_records()
#     return records

# # Белгілі бір дата + объектті жаңарту
# def update_booking_status(date, object_type, size, number, status, client="", phone="", notes=""):
#     records = sheet.get_all_records()
#     headers = sheet.row_values(1)

#     for idx, row in enumerate(records):
#         if (row["Date"] == date and row["Type"] == object_type and
#             row["Size"] == size and str(row["Number"]) == str(number)):
            
#             # Анықталған жол нөмірі (gspread 1-indexed)
#             row_number = idx + 2

#             # Қай бағанды жаңарту керек екенін білеміз:
#             updates = {
#                 "Status": status,
#                 "ClientName": client,
#                 "Phone": phone,
#                 "Notes": notes,
#             }

#             for col_name, value in updates.items():
#                 col_index = headers.index(col_name) + 1
#                 sheet.update_cell(row_number, col_index, value)
            
#             return True
    
#     return False