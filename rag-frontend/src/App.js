import React, { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [apiUrl, setApiUrl] = useState(process.env.REACT_APP_API_URL || "");
  // 🔴 Change this to your ngrok/cloudflared URL when deploying

  // Upload file
  const handleUpload = async () => {
    if (!file) return alert("Please select a file first!");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${apiUrl}/upload/`, {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Upload failed");
      const data = await res.json();
      alert(data.message);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  // Query documents
const handleQuery = async () => {
  if (!query) return alert("Please enter a query!");
  
  console.log("Sending to:", `${apiUrl}/query/`); // Debug URL
  console.log("Payload:", { query, top_k: 3 }); // Debug request body

  try {
    const res = await fetch(`${apiUrl}/query/`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
        "Accept": "application/json" // Explicitly ask for JSON
      },
      body: JSON.stringify({ query, top_k: 3 }),
    });

    console.log("Response status:", res.status); // Debug status code
    
    if (!res.ok) {
      const errorText = await res.text(); // Get full error response
      console.error("Full error response:", errorText);
      throw new Error(`Server responded with ${res.status}: ${errorText}`);
    }

    const contentType = res.headers.get("content-type");
    if (!contentType?.includes("application/json")) {
      const text = await res.text();
      console.warn("Received non-JSON response:", text);
      throw new Error("Server returned non-JSON response");
    }

    const data = await res.json();
    console.log("Full response data:", data); // Debug complete response

    // Simplified response handling
    setResults(
      data.results || 
      data.data || 
      (Array.isArray(data) ? data : [data]) // Fallback to array
    );
    
  } catch (err) {
    console.error("Complete error:", err);
    alert(`Query failed: ${err.message}`);
  }
};


  return (
    <div className="App">
      <h1>📄 RAG Document Assistant</h1>

      {/* API URL setter */}
      <div className="section">
        <label>Backend API URL: </label>
        <input
          type="text"
          value={apiUrl}
          onChange={(e) => setApiUrl(e.target.value)}
          placeholder="http://127.0.0.1:8000"
          style={{ width: "60%" }}
        />
      </div>

      {/* Upload */}
      <div className="section">
        <h2>Upload a Document</h2>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload}>Upload</button>
      </div>

      {/* Query */}
      <div className="section">
        <h2>Ask a Question</h2>
        <input
          type="text"
          placeholder="Type your query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleQuery}>Search</button>
      </div>

      {/* Results Table */}
      {results.length > 0 && (
        <div className="section">
          <h2>Results</h2>
          <table>
            <thead>
              <tr>
                <th>Document ID</th>
                <th>Theme</th>
                <th>Extracted Answer</th>
                <th>Citations</th>
              </tr>
            </thead>
            <tbody>
              {results.map((row, i) => (
                <tr key={i}>
                  <td>{row.document_id}</td>
                  <td>{row.theme}</td>
                  <td>{row.extracted_answer}</td>
                  <td>{row.citations}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
