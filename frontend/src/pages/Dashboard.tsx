// /home/sandeep/Projects/ScholarChat/frontend/src/pages/Dashboard.tsx
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/client";
import Layout from "../components/Layout";

type DocumentItem = {
  id: number;
  filename: string;
  upload_status: string;
  content?: string;
};

export default function Dashboard() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const navigate = useNavigate();

  const fetchDocuments = async () => {
    try {
      const res = await API.get("/documents/my");
      setDocuments(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    navigate("/");
  };

  const handleUpload = async () => {
    if (!selectedFile) return alert("Select file first");

    const allowed = [".pdf", ".docx", ".txt"];
    const ok = allowed.some((ext) =>
      selectedFile.name.toLowerCase().endsWith(ext)
    );

    if (!ok) return alert("Only PDF, DOCX, TXT allowed");

    const formData = new FormData();
    formData.append("file", selectedFile);

    await API.post("/documents/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    setSelectedFile(null);
    fetchDocuments();
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  return (
    <Layout>
      {/* HEADER */}
      <div className="content-header">
        <h1>Documents</h1>
        <button className="btn-outline" onClick={handleLogout}>
          Logout
        </button>
      </div>

      {/* UPLOAD SECTION */}
      <div className="card" style={{ marginBottom: "2rem" }}>
        <h2>Upload New Document</h2>
        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          Upload PDF, DOCX, or TXT files to start using your data.
        </p>

        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <input
            type="file"
            accept=".pdf,.docx,.txt"
            onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
            style={{ maxWidth: "400px" }}
          />

          <button className="btn-primary" onClick={handleUpload}>
            📤 Upload
          </button>
        </div>
      </div>

      {/* DOCUMENT GRID */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
          gap: "1.5rem",
        }}
      >
        {documents.map((doc) => (
          <div key={doc.id} className="card">
            {/* FILE NAME */}
            <div
              style={{
                fontSize: "1.1rem",
                fontWeight: 600,
                marginBottom: "0.5rem",
                whiteSpace: "nowrap",
                overflow: "hidden",
                textOverflow: "ellipsis",
              }}
              title={doc.filename}
            >
              📄 {doc.filename}
            </div>

            {/* STATUS */}
            <p
              style={{
                fontSize: "0.85rem",
                color: "#6b7280",
                marginBottom: "0.75rem",
              }}
            >
              Status:{" "}
              <span
                style={{
                  color:
                    doc.upload_status === "ready"
                      ? "#10b981"
                      : doc.upload_status === "processing"
                      ? "#f59e0b"
                      : "#ef4444",
                  fontWeight: 600,
                }}
              >
                {doc.upload_status}
              </span>
            </p>

            {/* CONTENT PREVIEW */}
            {doc.content && (
              <div
                style={{
                  fontSize: "0.85rem",
                  color: "#374151",
                  background: "#f8fafc",
                  padding: "0.75rem",
                  borderRadius: "8px",
                  marginBottom: "1rem",
                  lineHeight: "1.5",
                  maxHeight: "120px",
                  overflow: "hidden",
                  whiteSpace: "pre-wrap",
                }}
              >
                {doc.content.slice(0, 250)}...
              </div>
            )}

            {/* VIEW FULL DOC ONLY */}
            <button
              onClick={() => navigate(`/documents/${doc.id}`)}
              className="btn-outline"
              style={{
                width: "100%",
                textAlign: "center",
              }}
            >
              📘 View Full Document
            </button>
          </div>
        ))}

        {/* EMPTY STATE */}
        {documents.length === 0 && (
          <div
            style={{
              gridColumn: "1 / -1",
              textAlign: "center",
              padding: "4rem",
              color: "var(--text-muted)",
            }}
          >
            <div style={{ fontSize: "3rem", marginBottom: "1rem" }}>📂</div>
            <p>No documents found. Upload your first document to get started!</p>
          </div>
        )}
      </div>
    </Layout>
  );
}