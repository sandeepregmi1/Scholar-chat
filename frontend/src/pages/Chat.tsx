import { useState, useEffect, useRef } from "react";
import Layout from "../components/Layout";
import DocumentSelector from "../components/DocumentSelector";

type Message = {
  sender: "user" | "ai";
  text: string;
};

export default function Chat() {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const [documentId, setDocumentId] = useState<number | null>(null);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleAsk = async () => {
    if (!question.trim()) return;

    if (!documentId) {
      alert("Please select a document first");
      return;
    }

    const token = localStorage.getItem("token");

    if (!token) {
      alert("Please login first");
      return;
    }

    const userQuestion = question;

    // Add user message
    setMessages((prev) => [
      ...prev,
      { sender: "user", text: userQuestion },
    ]);

    setQuestion("");
    setLoading(true);

    // Add empty AI bubble for streaming
    setMessages((prev) => [
      ...prev,
      { sender: "ai", text: "" },
    ]);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/chat/ask?question=${encodeURIComponent(
          userQuestion
        )}&document_id=${documentId}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!response.body) throw new Error("No response stream");

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");

      let aiText = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        aiText += chunk;

        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            sender: "ai",
            text: aiText,
          };
          return updated;
        });
      }
    } catch (err) {
      console.error(err);

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          sender: "ai",
          text: "Error: Failed to get response",
        };
        return updated;
      });
    }

    setLoading(false);
  };

  return (
    <Layout>
      <div className="content-header">
        <h1>AI Chat</h1>
      </div>

      <DocumentSelector selectedId={documentId} onSelect={setDocumentId} />

      <div
        className="card"
        style={{
          height: "calc(100vh - 300px)",
          display: "flex",
          flexDirection: "column",
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
                marginTop: "4rem",
                color: "#9ca3af",
              }}
            >
              <div style={{ fontSize: "3rem" }}>💬</div>
              <p>Select a document and start chatting</p>
            </div>
          )}

          {messages.map((msg, i) => (
            <div
              key={i}
              className={msg.sender === "user" ? "user-bubble" : "ai-bubble"}
            >
              {msg.text}
            </div>
          ))}

          <div ref={messagesEndRef} />
        </div>

        {/* INPUT */}
        <div
          style={{
            display: "flex",
            gap: "1rem",
            padding: "1rem",
            borderTop: "1px solid #e5e7eb",
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
            placeholder="Ask something about this document..."
            style={{
              flex: 1,
              padding: "0.75rem",
              borderRadius: "8px",
              resize: "none",
            }}
          />

          <button
            className="btn-primary"
            onClick={handleAsk}
            disabled={loading || !question.trim()}
          >
            {loading ? "Thinking..." : "Send"}
          </button>
        </div>
      </div>
    </Layout>
  );
}