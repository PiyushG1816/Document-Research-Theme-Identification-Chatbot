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
  try {
    const res = await fetch(`${apiUrl}/query/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, top_k: 3 }),
    });

    if (!res.ok) throw new Error("Query failed");

    const data = await res.json();
    console.log("Query response:", data); // 👈 check exact structure in console

    // Handle possible response shapes
    if (Array.isArray(data)) {
      setResults(data);
    } else if (data.results) {
      setResults(data.results);
    } else if (data.data) {
      setResults(data.data);
    } else {
      console.warn("Unexpected response shape:", data);
      setResults([]);
    }
  } catch (err) {
    console.error(err);
    alert("Query failed");
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
