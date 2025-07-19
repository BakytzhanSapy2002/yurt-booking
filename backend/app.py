from flask import Flask, jsonify, request
from flask_cors import CORS
from sheets_api import get_calendar_data, update_booking_status, update_status as update_status_in_sheet
from update_calendar_data import update_sheet

app = Flask(__name__)
CORS(app)
# 🔐 Логин тексеру маршруты
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == "SapyDoszhan" and password == "13041993":
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 401
# ✅ Барлық бронь жазбаларын алу
@app.route("/api/calendar", methods=["GET"])
def calendar():
    data = get_calendar_data()
    return jsonify(data)

# ✅ Объект статустарын жаңарту (1-нұсқа – резерв)
@app.route("/api/update", methods=["POST"])
def update():
    try:
        payload = request.get_json()
        required_fields = ["date", "type", "size", "number", "status"]

        if not all(k in payload for k in required_fields):
            return jsonify({"error": "Missing fields"}), 400

        result = update_booking_status(
            payload["date"],
            payload["type"],
            payload["size"],
            payload["number"],
            payload["status"],
            payload.get("client", ""),
            payload.get("phone", ""),
            payload.get("notes", "")
        )

        if result:
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Object not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Екінші маршрут (React батырма үшін)
@app.route('/api/update_status', methods=['POST'])
def update_status_endpoint():
    data = request.get_json()
    date = data.get('Date')
    obj_type = data.get('Type')
    size = data.get('Size')
    number = data.get('Number')
    new_status = data.get('Status')
    client = data.get('ClientName', '')
    phone = data.get('Phone', '')
    notes = data.get('Notes', '')

    updated = update_status_in_sheet(date, obj_type, size, number, new_status, client, phone, notes)
    return jsonify({"success": updated})

# ✅ Flask сервері іске қосылғанда бір реттік жаңарту орындалады
if __name__ == "__main__":
    print("🔄 Күнтізбе жаңартылып жатыр...")
    update_sheet()  # ← Міне, дәл осы жерде Google Sheets-тағы деректер жаңарады
    print("✅ Жаңарту аяқталды.")
    app.run(debug=True)
