// /src/pages/Notes.tsx

import { useState } from "react";
import Layout from "../components/Layout";
import API from "../api/client";
import DocumentSelector from "../components/DocumentSelector";

type Note = {
  title: string;
  content: string;
};

export default function Notes() {
  const [topic, setTopic] = useState("");
  const [selectedDoc, setSelectedDoc] = useState<number | null>(null);

  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(false);

  const generateNotes = async () => {
    if (!topic.trim()) return alert("Enter topic");
    if (selectedDoc === null) return alert("Select a document");

    setLoading(true);
    setNotes([]);

    try {
      const res = await API.post("/notes/generate", null, {
        params: {
          topic,
          document_id: selectedDoc,
        },
      });

      const data = res.data?.notes;

      // ✅ SAFE NORMALIZATION (prevents crash)
      const normalizedNotes: Note[] = Array.isArray(data)
        ? data
        : data
        ? [
            {
              title: "Generated Notes",
              content: String(data),
            },
          ]
        : [];

      setNotes(normalizedNotes);
    } catch (err) {
      console.error("Failed to generate notes:", err);
      alert("Failed to generate notes");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="content-header">
        <h1>Notes Workspace</h1>
      </div>

      {/* DOCUMENT SELECTOR */}
      <DocumentSelector
        selectedId={selectedDoc}
        onSelect={setSelectedDoc}
      />

      {/* INPUT */}
      <div className="card" style={{ marginBottom: "2rem" }}>
        <h2>Generate AI Notes</h2>

        <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
          <input
            style={{ flex: 1 }}
            placeholder="Topic (e.g. Quantum Computing)"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />

          <button
            className="btn-primary"
            onClick={generateNotes}
            disabled={loading || !topic.trim() || selectedDoc === null}
          >
            {loading ? "Generating..." : "Generate Notes"}
          </button>
        </div>

        {selectedDoc !== null && (
          <p style={{ marginTop: "0.75rem", fontSize: "0.85rem", color: "#6b7280" }}>
            Selected Document ID: <b>{selectedDoc}</b>
          </p>
        )}
      </div>

      {/* OUTPUT */}
      <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
        {notes.length > 0 ? (
          notes.map((note, i) => (
            <div key={i} className="card">
              <h3 style={{ marginBottom: "0.5rem" }}>{note.title}</h3>
              <p style={{ whiteSpace: "pre-wrap", lineHeight: "1.6" }}>
                {note.content}
              </p>
            </div>
          ))
        ) : (
          !loading && (
            <div
              style={{
                textAlign: "center",
                padding: "4rem",
                color: "#9ca3af",
              }}
            >
              <div style={{ fontSize: "3rem" }}>📒</div>
              <p>No notes generated yet</p>
            </div>
          )
        )}
      </div>
    </Layout>
  );
}