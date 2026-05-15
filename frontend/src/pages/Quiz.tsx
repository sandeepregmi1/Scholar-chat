import { useState } from "react";
import Layout from "../components/Layout";
import API from "../api/client";
import DocumentSelector from "../components/DocumentSelector";

type Question = {
  question: string;
  options: string[];
  answer: string;
};

type QuizResult = {
  score: number;
  total: number;
  percentage: number;
};

export default function Quiz() {
  const [topic, setTopic] = useState("");
  const [selectedDoc, setSelectedDoc] = useState<number | null>(null);

  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(false);

  const [current, setCurrent] = useState(0);
  const [score, setScore] = useState(0);
  const [selected, setSelected] = useState<string | null>(null);
  const [finished, setFinished] = useState(false);
  const [result, setResult] = useState<QuizResult | null>(null);

  const saveResult = (data: QuizResult) => {
    localStorage.setItem("quiz_result", JSON.stringify(data));
  };

  // normalize helper (VERY IMPORTANT FIX)
  const normalize = (text: string) =>
    text
      .toLowerCase()
      .replace(/\(correct answer\)/gi, "")
      .replace(/answer\s*:/gi, "")
      .replace(/[^\w\s]/g, "")
      .trim();

  const parseTextQuiz = (rawText: string): Question[] => {
    const blocks = rawText.split(/\n(?=Q[:\d])/i);

    return blocks
      .map((block) => {
        const lines = block
          .split("\n")
          .map((l) => l.trim())
          .filter(Boolean);

        if (!lines.length) return null;

        const question = lines[0].replace(/^Q[:\d.\s-]*/i, "").trim();

        const options = lines
          .filter((l) => /^[A-D][).:-]/i.test(l))
          .map((l) => l.replace(/^[A-D][).:-]\s*/i, "").trim());

        const answerLine = lines.find((l) =>
          l.toLowerCase().startsWith("answer")
        );

        const answer = answerLine
          ? answerLine.split(":").slice(1).join(":").trim()
          : options[0] || "";

        return { question, options, answer };
      })
      .filter(Boolean) as Question[];
  };

  const generateQuiz = async () => {
    if (!topic.trim()) return alert("Enter topic");
    if (selectedDoc === null) return alert("Select a document");

    setLoading(true);
    setQuestions([]);
    setCurrent(0);
    setScore(0);
    setSelected(null);
    setFinished(false);
    setResult(null);

    try {
      const res = await API.post("/quiz/generate", null, {
        params: {
          topic,
          document_id: selectedDoc,
        },
      });

      const data = res.data?.quiz;

      let normalized: Question[] = [];

      if (Array.isArray(data)) {
        normalized = data.map((q: any) => ({
          question: q?.question ?? "Question",
          options: Array.isArray(q?.options) ? q.options : [],
          answer: q?.answer ?? "",
        }));
      } else if (typeof data === "string") {
        normalized = parseTextQuiz(data);
      }

      setQuestions(normalized);
    } catch (err) {
      console.error(err);
      alert("Failed to generate quiz");
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (option: string) => {
    if (selected || !questions[current]) return;

    setSelected(option);

    const correct = questions[current].answer;

    const isCorrect =
      normalize(option) === normalize(correct);

    if (isCorrect) {
      setScore((prev) => prev + 1);
    }

    setTimeout(() => {
      if (current + 1 < questions.length) {
        setCurrent((p) => p + 1);
        setSelected(null);
      } else {
        const finalScore = isCorrect
          ? score + 1
          : score;

        const resultData: QuizResult = {
          score: finalScore,
          total: questions.length,
          percentage: Math.round(
            (finalScore / questions.length) * 100
          ),
        };

        setResult(resultData);
        saveResult(resultData);
        setFinished(true);
      }
    }, 800);
  };

  const handleRetry = () => {
    setCurrent(0);
    setScore(0);
    setSelected(null);
    setFinished(false);
    setResult(null);
  };

  const currentQ = questions[current];

  return (
    <Layout>
      <div className="content-header">
        <h1>Quiz Mode</h1>
      </div>

      <DocumentSelector
        selectedId={selectedDoc}
        onSelect={setSelectedDoc}
      />

      <div className="card">
        <h2>Take a Quiz</h2>

        <div style={{ display: "flex", gap: "1rem" }}>
          <input
            style={{ flex: 1 }}
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Topic..."
          />

          <button
            className="btn-primary"
            disabled={loading}
            onClick={generateQuiz}
          >
            {loading ? "Generating..." : "Start Quiz"}
          </button>
        </div>
      </div>

      {result && (
        <div className="card" style={{ textAlign: "center" }}>
          <h2>🎯 Results</h2>
          <div style={{ fontSize: "3rem" }}>
            {result.percentage}%
          </div>
          <p>
            Score: {result.score} / {result.total}
          </p>

          <button className="btn-primary" onClick={handleRetry}>
            Retry
          </button>
        </div>
      )}

      {!finished && currentQ && (
        <div className="card">
          <h3>
            Q{current + 1} / {questions.length}
          </h3>

          <p style={{ fontSize: "1.2rem" }}>
            {currentQ.question}
          </p>

          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {currentQ.options.map((opt, i) => {
              const correct = currentQ.answer;

              const isCorrect =
                normalize(opt) === normalize(correct);

              const isSelected = selected === opt;

              return (
                <div
                  key={i}
                  onClick={() => handleAnswer(opt)}
                  style={{
                    padding: "12px",
                    border: "2px solid",
                    borderRadius: 10,
                    cursor: selected ? "default" : "pointer",
                    borderColor: !selected
                      ? "#ccc"
                      : isCorrect
                      ? "#10b981"
                      : isSelected
                      ? "#ef4444"
                      : "#ccc",

                    background:
                      selected && isCorrect
                        ? "#ecfdf5"
                        : selected && isSelected
                        ? "#fef2f2"
                        : "white",
                  }}
                >
                  {opt}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {!loading && questions.length === 0 && (
        <div style={{ textAlign: "center", marginTop: 40 }}>
          🧠 Select a document and generate quiz
        </div>
      )}
    </Layout>
  );
}