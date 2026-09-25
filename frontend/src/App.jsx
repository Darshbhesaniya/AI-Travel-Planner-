import { useState } from "react";

import React from 'react'

const App = () => {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const testBackend = async () => {
    try {
      setLoading(true);

      const response = await fetch("http://localhost:5000/api/hello");
      const data = await response.json();

      setMessage(data.message);
    } catch (error) {
      console.error(error);
      setMessage("Failed to connect to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
   <div>
      <h1>AI Travel Planner</h1>

      <button onClick={testBackend}>
        {loading ? "Connecting..." : "Test Backend"}
      </button>

      {message && <p>{message}</p>}
    </div>
  )
}

export default App