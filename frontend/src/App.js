import React, { useState, useEffect } from "react";
import LoginModal from "./LoginModal";

function App() {
  const [isAdmin, setIsAdmin] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [data, setData] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedObject, setSelectedObject] = useState(null);

  // API-дан деректерді алу
  useEffect(() => {
    fetch("http://localhost:5000/api/calendar")
      .then((res) => res.json())
      .then((data) => setData(data))
      .catch((err) => console.error("Дерек алу қатесі:", err));
  }, []);

  // Уникалды күндер тізімі
  const dates = [...new Set(data.map((item) => item.Date))];

  // Күнге сай броньдарды фильтрлеу
  const filtered = selectedDate
    ? data.filter((item) => item.Date === selectedDate)
    : [];

  // Объектілерді топтау
  const grouped = {
    "Кіші тапчан (8000 тг)": [],
    "Үлкен тапчан (15000 тг)": [],
    "Кіші киіз үй (25000 тг)": [],
    "Үлкен киіз үй (40000 тг)": [],
  };

  filtered.forEach((item) => {
    if (item.Type === "Tapchan" && item.Size === "Small") grouped["Кіші тапчан (8000 тг)"].push(item);
    if (item.Type === "Tapchan" && item.Size === "Large") grouped["Үлкен тапчан (15000 тг)"].push(item);
    if (item.Type === "Yurt" && item.Size === "Small") grouped["Кіші киіз үй (25000 тг)"].push(item);
    if (item.Type === "Yurt" && item.Size === "Large") grouped["Үлкен киіз үй (40000 тг)"].push(item);
  });

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h2>🏕 Броньдау жүйесі</h2>

      {/* 🔑 Кіру */}
      {!isAdmin && (
        <button onClick={() => setShowLogin(true)}>🔑 Кіру (админ)</button>
      )}
      {showLogin && (
        <LoginModal
          onClose={() => setShowLogin(false)}
          onSuccess={() => setIsAdmin(true)}
        />
      )}

      <hr />

      {/* 📅 Күндер */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: "5px" }}>
        {dates.map((d) => (
          <button
            key={d}
            style={{
              padding: "8px",
              backgroundColor: selectedDate === d ? "#2196F3" : "#eee",
              color: selectedDate === d ? "white" : "black",
              borderRadius: "5px",
              border: "1px solid #ccc",
            }}
            onClick={() => {
              setSelectedDate(d);
              setSelectedObject(null);
            }}
          >
            {d}
          </button>
        ))}
      </div>

      {/* ⛺ Объектілер тізімі */}
      {selectedDate && (
        <div style={{ marginTop: "20px" }}>
          <h3>📆 Таңдалған күн: {selectedDate}</h3>
          {Object.entries(grouped).map(([label, items]) => (
            <div key={label} style={{ marginBottom: "15px" }}>
              <strong>{label}</strong>
              <div style={{ display: "flex", gap: "5px", flexWrap: "wrap" }}>
                {items.map((obj, idx) => (
                  <div
                    key={idx}
                    style={{
                      width: "50px",
                      height: "50px",
                      backgroundColor: obj.Status === "free" ? "green" : "red",
                      color: "white",
                      display: "flex",
                      justifyContent: "center",
                      alignItems: "center",
                      borderRadius: "5px",
                      cursor: "pointer",
                    }}
                    onClick={() => setSelectedObject(obj)}
                  >
                    {obj.Number}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* ℹ️ Объект мәліметі */}
      {selectedObject && (
        <div style={{ marginTop: "20px", padding: "15px", border: "1px solid #ccc", borderRadius: "8px" }}>
          <h4>🧾 Объект мәліметі</h4>
          <p>Күн: {selectedObject.Date}</p>
          <p>Түрі: {selectedObject.Type === "Tapchan" ? "Тапчан" : "Киіз үй"}</p>
          <p>Өлшемі: {selectedObject.Size === "Small" ? "Кіші" : "Үлкен"}</p>
          <p>Нөмірі: {selectedObject.Number}</p>
          <p>Бағасы: {selectedObject.Price} тг</p>
          <p>Статус: {selectedObject.Status === "free" ? "Бос" : "Броньдалған"}</p>
          {selectedObject.Status === "booked" && (
            <>
              <p>Клиент: {selectedObject.ClientName}</p>
              <p>Телефон: {selectedObject.Phone}</p>
              <p>Ескерту: {selectedObject.Notes}</p>
            </>
          )}

          {/* 🔐 Тек админ үшін батырма */}
          {isAdmin && (
            <button
              style={{
                marginTop: "10px",
                padding: "10px",
                backgroundColor: selectedObject.Status === "free" ? "#2196F3" : "#FFC107",
                color: "white",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
              }}
              onClick={async () => {
                const newStatus = selectedObject.Status === "free" ? "booked" : "free";
                const updated = {
                  ...selectedObject,
                  Status: newStatus,
                  ClientName:
                    newStatus === "booked"
                      ? prompt("Клиент аты:", selectedObject.ClientName) || ""
                      : "",
                  Phone:
                    newStatus === "booked"
                      ? prompt("Телефон нөмірі:", selectedObject.Phone) || ""
                      : "",
                  Notes:
                    newStatus === "booked"
                      ? prompt("Ескерту:", selectedObject.Notes) || ""
                      : "",
                };

                const res = await fetch("http://localhost:5000/api/update_status", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(updated),
                });

                const result = await res.json();
                if (result.success) {
                  alert("✅ Статус сәтті жаңартылды!");
                  setData((prev) =>
                    prev.map((item) =>
                      item.Date === updated.Date &&
                      item.Type === updated.Type &&
                      item.Size === updated.Size &&
                      item.Number === updated.Number
                        ? updated
                        : item
                    )
                  );
                  setSelectedObject(updated);
                } else {
                  alert("❌ Жаңарту кезінде қате шықты.");
                }
              }}
            >
              {selectedObject.Status === "free" ? "🔐 Бронь жасау" : "❌ Босату"}
            </button>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
