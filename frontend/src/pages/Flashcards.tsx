// /src/pages/Flashcards.tsx

import { useState } from "react";
import Layout from "../components/Layout";
import API from "../api/client";
import DocumentSelector from "../components/DocumentSelector";

type Flashcard = {
  question: string;
  answer: string;
};

export default function Flashcards() {
  const [topic, setTopic] = useState("");
  const [selectedDoc, setSelectedDoc] = useState<number | null>(null);

  const [cards, setCards] = useState<Flashcard[]>([]);
  const [loading, setLoading] = useState(false);
  const [flipped, setFlipped] = useState<number | null>(null);

  const generateFlashcards = async () => {
    if (!topic.trim()) return alert("Enter topic");
    if (selectedDoc === null) return alert("Select a document");

    setLoading(true);
    setCards([]);
    setFlipped(null);

    try {
      const res = await API.post("/flashcards/generate", null, {
        params: {
          topic,
          document_id: selectedDoc,
        },
      });

      const data = res.data?.flashcards;
      let normalizedCards: Flashcard[] = [];

      // if backend already returns array
      if (Array.isArray(data)) {
        normalizedCards = data.map((item: any) => ({
          question: item?.question ?? "Question unavailable",
          answer: item?.answer ?? String(item),
        }));
      }

      // if backend returns long string
      else if (typeof data === "string") {
        const parts = data.split("Q:").filter(Boolean);

        normalizedCards = parts.map((part: string) => {
          const [q, a] = part.split("A:");

          return {
            question: q?.trim() || "Question",
            answer: a?.trim() || "Answer",
          };
        });
      }

      setCards(normalizedCards);
    } catch (err) {
      console.error("Failed to generate flashcards:", err);
      alert("Failed to generate flashcards");
    } finally {
      setLoading(false);
    }
  };

  const isDisabled = loading || !topic.trim() || selectedDoc === null;

  return (
    <Layout>
      <div className="content-header">
        <h1>Flashcards</h1>
      </div>

      <DocumentSelector
        selectedId={selectedDoc}
        onSelect={setSelectedDoc}
      />

      <div className="card" style={{ marginBottom: "2rem" }}>
        <h2>Create Flashcards</h2>
        <p style={{ color: "var(--text-muted)", marginBottom: "1rem" }}>
          Generate flashcards from a selected document
        </p>

        <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
          <input
            style={{ flex: 1 }}
            placeholder="Topic (e.g. AI in Agriculture)"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />

          <button
            className="btn-primary"
            onClick={generateFlashcards}
            disabled={isDisabled}
          >
            {loading ? "Generating..." : "Generate Flashcards"}
          </button>
        </div>

        {selectedDoc !== null && (
          <p style={{ marginTop: "0.75rem", fontSize: "0.85rem", color: "#6b7280" }}>
            Selected Document ID: <b>{selectedDoc}</b>
          </p>
        )}
      </div>

      <div
        style={{
          display: "grid",
          gap: "1.5rem",
        }}
      >
        {cards.map((card, index) => (
          <div
            key={index}
            className="card"
            onClick={() => setFlipped(flipped === index ? null : index)}
            style={{
              minHeight: "220px",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: "1.5rem",
              borderRadius: "12px",
              background: flipped === index ? "#111827" : "white",
              color: flipped === index ? "white" : "#111827",
              transition: "all 0.3s ease",
            }}
          >
            <div>
              {flipped === index ? (
                <>
                  <div style={{ fontSize: "0.75rem", opacity: 0.7 }}>
                    Answer
                  </div>
                  <div
                    style={{
                      marginTop: "0.75rem",
                      lineHeight: "1.6",
                      whiteSpace: "pre-wrap",
                    }}
                  >
                    {card.answer}
                  </div>
                </>
              ) : (
                <>
                  <div style={{ fontSize: "0.75rem", opacity: 0.7 }}>
                    Question
                  </div>
                  <div
                    style={{
                      marginTop: "0.75rem",
                      lineHeight: "1.6",
                      whiteSpace: "pre-wrap",
                    }}
                  >
                    {card.question}
                  </div>
                </>
              )}
            </div>
          </div>
        ))}

        {!loading && cards.length === 0 && (
          <div
            style={{
              gridColumn: "1 / -1",
              textAlign: "center",
              padding: "4rem",
              color: "#9ca3af",
            }}
          >
            <div style={{ fontSize: "3rem" }}>⚡</div>
            <p>No flashcards generated yet</p>
          </div>
        )}
      </div>
    </Layout>
  );
}