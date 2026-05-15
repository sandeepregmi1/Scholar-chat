import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import API from "../api/client";
import Layout from "../components/Layout";

type DocumentItem = {
  id: number;
  filename: string;
  upload_status: string;
  content?: string;
  file_size?: number;
  created_at?: string;
};

export default function DocumentDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [doc, setDoc] = useState<DocumentItem | null>(null);

  const fetchDocument = async () => {
    try {
      const res = await API.get(`/documents/my`);
      const found = res.data.find((d: DocumentItem) => d.id === Number(id));
      setDoc(found);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchDocument();
  }, [id]);

  if (!doc) {
    return (
      <Layout>
        <div style={{ padding: "2rem" }}>Loading document...</div>
      </Layout>
    );
  }

  return (
    <Layout>
      <button
        onClick={() => navigate(-1)}
        className="btn-outline"
        style={{ marginBottom: "1rem" }}
      >
        ← Back
      </button>

      <div className="card">
        <h1 style={{ marginBottom: "0.5rem" }}>📄 {doc.filename}</h1>

        <p style={{ color: "#6b7280", marginBottom: "1rem" }}>
          Status: <b>{doc.upload_status}</b>
        </p>

        {doc.file_size && (
          <p style={{ color: "#6b7280", marginBottom: "1rem" }}>
            Size: {(doc.file_size / 1024).toFixed(2)} KB
          </p>
        )}

        <hr style={{ margin: "1rem 0" }} />

        <h3>Document Content</h3>

        <div
          style={{
            whiteSpace: "pre-wrap",
            background: "#f8fafc",
            padding: "1rem",
            borderRadius: "10px",
            marginTop: "1rem",
            lineHeight: "1.6",
            fontSize: "0.95rem",
          }}
        >
          {doc.content || "No content available"}
        </div>
      </div>
    </Layout>
  );
}