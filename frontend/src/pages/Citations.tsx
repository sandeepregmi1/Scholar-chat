// /src/pages/Citations.tsx

import { useState } from "react";
import Layout from "../components/Layout";
import API from "../api/client";
import DocumentSelector from "../components/DocumentSelector";

type Citation = {
  document_id: number;
  page_number?: number;
  score?: number;
};

export default function Citations() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState<Citation[]>([]);
  const [loading, setLoading] = useState(false);

  const [selectedDoc, setSelectedDoc] = useState<number | null>(null);

  const ask = async () => {
    if (!question.trim()) return;
    if (!selectedDoc) return alert("Please select a document first");

    setLoading(true);
    setAnswer("");
    setCitations([]);

    try {
      const res = await API.post("/citations/ask", null, {
        params: {
          question,
          document_id: selectedDoc,
        },
      });

      setAnswer(res.data?.answer || "");
      setCitations(res.data?.citations || []);
    } catch (err) {
      console.error(err);
      alert("Failed to fetch citations");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="content-header">
        <h1>Answer with Citations</h1>
      </div>

      {/* DOCUMENT SELECTOR (FIXED) */}
      <DocumentSelector
        selectedId={selectedDoc}
        onSelect={setSelectedDoc}
      />

      {/* INPUT */}
      <div className="card" style={{ marginBottom: "2rem" }}>
        <h2>Ask a Question</h2>

        <div style={{ display: "flex", gap: "1rem" }}>
          <input
            style={{ flex: 1 }}
            placeholder="Ask something..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && ask()}
          />

          <button
            className="btn-primary"
            onClick={ask}
            disabled={loading}
          >
            {loading ? "Thinking..." : "Ask"}
          </button>
        </div>
      </div>

      {/* ANSWER */}
      {answer && (
        <div className="card" style={{ marginBottom: "2rem" }}>
          <h3>Answer</h3>
          <p style={{ whiteSpace: "pre-wrap", lineHeight: "1.6" }}>
            {answer}
          </p>
        </div>
      )}

      {/* CITATIONS */}
      {citations.length > 0 && (
        <div className="card">
          <h3>Sources / Citations</h3>

          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            {citations.map((c, i) => (
              <div
                key={i}
                style={{
                  padding: "1rem",
                  border: "1px solid #e5e7eb",
                  borderRadius: "8px",
                  background: "#f9fafb",
                }}
              >
                <p>
                  📄 Document ID: <b>{c.document_id}</b>
                </p>

                {c.page_number && (
                  <p>📑 Page: {c.page_number}</p>
                )}

                {c.score !== undefined && (
                  <p>📊 Relevance: {c.score.toFixed(2)}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* EMPTY STATE */}
      {!loading && !answer && (
        <div
          style={{
            textAlign: "center",
            marginTop: "4rem",
            color: "#9ca3af",
          }}
        >
          <div style={{ fontSize: "3rem" }}>📚</div>
          <p>Select a document and ask a question to see citations</p>
        </div>
      )}
    </Layout>
  );
}