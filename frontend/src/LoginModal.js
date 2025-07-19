import React, { useState } from "react";

function LoginModal({ onClose, onSuccess }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    const res = await fetch("http://localhost:5000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (res.ok) {
      alert("✅ Сәтті кірдіңіз!");
      onSuccess(); // setIsAdmin true болады
      onClose();
    } else {
      alert("❌ Қате логин немесе құпия сөз");
    }
  };

  return (
    <div style={{
      backgroundColor: "#fff", padding: "20px", borderRadius: "10px",
      boxShadow: "0 0 10px rgba(0,0,0,0.2)", maxWidth: "300px", margin: "auto"
    }}>
      <h3>🔐 Админ кірісі</h3>
      <input
        type="text"
        placeholder="Логин"
        value={username}
        onChange={e => setUsername(e.target.value)}
        style={{ marginBottom: "10px", width: "100%" }}
      />
      <input
        type="password"
        placeholder="Құпия сөз"
        value={password}
        onChange={e => setPassword(e.target.value)}
        style={{ marginBottom: "10px", width: "100%" }}
      />
      <button onClick={handleLogin} style={{ marginRight: "10px" }}>Кіру</button>
      <button onClick={onClose}>Жабу</button>
    </div>
  );
}

export default LoginModal;
