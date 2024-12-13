import React, { useEffect, useState } from "react";
import { fetchHelloMessage } from "./api";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const getMessage = async () => {
      try {
        const data = await fetchHelloMessage();
        setMessage(data.message);
      } catch (error) {
        console.error("Error fetching message:", error);
      }
    };

    getMessage();
  }, []);

  return (
    <div>
      <h1>React and Flask Integration</h1>
      <p>{message || "Loading..."}</p>
    </div>
  );
}

export default App;
