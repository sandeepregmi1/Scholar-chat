// /src/pages/MultiChat.tsx

import { useState, useEffect, useRef } from "react";
import API from "../api/client";
import Layout from "../components/Layout";

type Message = {
  role: "user" | "ai";
  text: string;
};

type DocumentItem = {
  id: number;
  filename: string;
  upload_status: string;
};

export default function MultiChat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [selectedDocs, setSelectedDocs] = useState<number[]>([]);
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // ✅ fetch documents safely
  const fetchDocuments = async () => {
    try {
      const res = await API.get("/documents/my");
      setDocuments(res.data || []);
    } catch (err) {
      console.error("Failed to load documents", err);
      setDocuments([]);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const toggleDoc = (id: number) => {
    setSelectedDocs((prev) =>
      prev.includes(id)
        ? prev.filter((d) => d !== id)
        : [...prev, id]
    );
  };

  const handleAsk = async () => {
    if (!question.trim()) return;

    if (selectedDocs.length === 0) {
      alert("Please select at least one document");
      return;
    }

    setLoading(true);

    setMessages((prev) => [
      ...prev,
      { role: "user", text: question },
    ]);

    const currentQuestion = question;
    setQuestion("");

    try {
      const response = await API.post("/multi-chat/ask", null, {
        params: {
          question: currentQuestion,
          document_ids: selectedDocs.join(","),
        },
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: response.data?.answer || "No response",
        },
      ]);
    } catch (err) {
      console.error(err);
      alert("Multi-chat failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="content-header">
        <h1>Multi Chat</h1>
      </div>

      {/* DOCUMENT SELECTOR */}
      <div className="card" style={{ marginBottom: "2rem" }}>
        <h2>Chat with Multiple Documents</h2>

        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          Synthesize information from multiple sources simultaneously.
        </p>

        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.75rem" }}>
          {documents.map((doc) => {
            const isSelected = selectedDocs.includes(doc.id);

            return (
              <label
                key={doc.id}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "0.5rem",
                  padding: "0.5rem 1rem",
                  border: "1px solid var(--border-color)",
                  borderRadius: "8px",
                  cursor: "pointer",
                  background: isSelected ? "#eef2ff" : "white",
                }}
              >
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => toggleDoc(doc.id)}
                />
                📄 {doc.filename}
              </label>
            );
          })}
        </div>

        {selectedDocs.length > 0 && (
          <p style={{ marginTop: "1rem", fontSize: "0.85rem" }}>
            Selected Documents: <b>{selectedDocs.join(", ")}</b>
          </p>
        )}
      </div>

      {/* CHAT AREA */}
      <div
        className="card"
        style={{
          height: "calc(100vh - 350px)",
          display: "flex",
          flexDirection: "column",
          padding: "1rem",
        }}
      >
        {/* MESSAGES */}
        <div
          style={{
            flex: 1,
            overflowY: "auto",
            padding: "1rem",
            display: "flex",
            flexDirection: "column",
            gap: "1rem",
          }}
        >
          {messages.length === 0 && (
            <div
              style={{
                textAlign: "center",
                color: "var(--text-muted)",
                marginTop: "4rem",
              }}
            >
              <div style={{ fontSize: "3rem" }}>🧠</div>
              <p>Choose documents and start chatting.</p>
            </div>
          )}

          {messages.map((msg, i) => (
            <div
              key={i}
              className={msg.role === "user" ? "user-bubble" : "ai-bubble"}
              style={{ whiteSpace: "pre-wrap" }}
            >
              {msg.text}
            </div>
          ))}

          {loading && (
            <div className="ai-bubble" style={{ opacity: 0.7 }}>
              🧠 Thinking across documents...
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* INPUT */}
        <div
          style={{
            marginTop: "1rem",
            paddingTop: "1rem",
            borderTop: "1px solid var(--border-color)",
            display: "flex",
            gap: "1rem",
          }}
        >
          <textarea
            rows={1}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleAsk();
              }
            }}
            placeholder="Ask across your documents..."
            style={{
              flex: 1,
              padding: "0.75rem 1rem",
              borderRadius: "8px",
            }}
          />

          <button
            className="btn-primary"
            onClick={handleAsk}
            disabled={loading || !question.trim()}
          >
            {loading ? "..." : "Send"}
          </button>
        </div>
      </div>
    </Layout>
  );
}