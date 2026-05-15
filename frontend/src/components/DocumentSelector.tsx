// /home/sandeep/Projects/ScholarChat/frontend/src/components/DocumentSelector.tsx
import { useEffect, useState } from "react";
import API from "../api/client";

export type DocumentItem = {
  id: number;
  filename: string;
  upload_status?: "ready" | "processing" | "failed" | string;
};

type Props = {
  selectedId: number | null;
  onSelect: (id: number) => void;
};

export default function DocumentSelector({ selectedId, onSelect }: Props) {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await API.get("/documents/my");
      setDocuments(res.data || []);
    } catch (err) {
      console.error("Failed to load documents", err);
      setError("Failed to load documents. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  return (
    <div className="card" style={{ marginBottom: "2rem" }}>
      <h2>Select Document</h2>

      <p style={{ color: "var(--text-muted)", marginBottom: "1rem" }}>
        Choose a document to generate notes, flashcards, quiz, or citations
      </p>

      {/* LOADING STATE */}
      {loading && <p style={{ color: "#6b7280" }}>Loading documents...</p>}

      {/* ERROR STATE */}
      {error && (
        <div style={{ marginBottom: "1rem", color: "#ef4444" }}>
          {error}
          <button
            onClick={fetchDocuments}
            style={{
              marginLeft: "1rem",
              padding: "4px 10px",
              border: "1px solid #ef4444",
              borderRadius: "6px",
              background: "transparent",
              cursor: "pointer",
            }}
          >
            Retry
          </button>
        </div>
      )}

      {/* DOCUMENT GRID */}
      {!loading && !error && (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))",
            gap: "1rem",
          }}
        >
          {documents.map((doc) => {
            const isSelected = selectedId === doc.id;

            return (
              <div
                key={doc.id}
                onClick={() => onSelect(doc.id)}
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === "Enter") onSelect(doc.id);
                }}
                style={{
                  padding: "1rem",
                  borderRadius: "12px",
                  border: isSelected
                    ? "2px solid #6366f1"
                    : "1px solid #e5e7eb",
                  background: isSelected ? "#eef2ff" : "white",
                  cursor: "pointer",
                  transition: "all 0.2s ease",
                  outline: "none",
                }}
              >
                <div style={{ fontWeight: 600, marginBottom: "0.5rem" }}>
                  📄 {doc.filename}
                </div>

                <div
                  style={{
                    fontSize: "0.8rem",
                    color:
                      doc.upload_status === "ready"
                        ? "#10b981"
                        : doc.upload_status === "processing"
                        ? "#f59e0b"
                        : doc.upload_status === "failed"
                        ? "#ef4444"
                        : "#6b7280",
                  }}
                >
                  Status: {doc.upload_status || "unknown"}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* EMPTY STATE */}
      {!loading && !error && documents.length === 0 && (
        <p style={{ color: "#9ca3af", marginTop: "1rem" }}>
          No documents found.
        </p>
      )}

      {/* SELECTED INFO */}
      {selectedId && (
        <p style={{ marginTop: "1rem", fontSize: "0.85rem" }}>
          Selected Document ID: <b>{selectedId}</b>
        </p>
      )}
    </div>
  );
}