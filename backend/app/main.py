"use client";

import { useState } from "react";

const defaultQuestions = [
  "Tell me about a project you led and the impact it had.",
  "How do you design a scalable backend for a product with growing traffic?",
  "Walk me through how you would optimize a slow SQL query.",
  "Describe a time when you handled ambiguity in a technical project.",
];

export default function InterviewPage() {
  const [questions, setQuestions] = useState(defaultQuestions);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState<null | {
    overall_score: number;
    technical_accuracy: number;
    communication: number;
    problem_solving: number;
    feedback: string;
    improvement_tip: string;
  }>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
      const response = await fetch(`${apiUrl}/api/mock-interview/evaluate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: questions[currentIndex],
          answer,
        }),
      });

      if (!response.ok) {
        throw new Error("Unable to evaluate answer.");
      }

      const data = await response.json();
      setEvaluation(data);
    } catch (error) {
      console.error(error);
      setEvaluation({
        overall_score: 0,
        technical_accuracy: 0,
        communication: 0,
        problem_solving: 0,
        feedback: "Evaluation failed. Please try again.",
        improvement_tip: "Ensure your answer includes technical depth and a clear structure.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const nextQuestion = () => {
    setEvaluation(null);
    setAnswer("");
    setCurrentIndex((prev) => (prev + 1) % questions.length);
  };

  return (
    <main className="page-shell inner-page">
      <div className="section-header">
        <h1>AI Mock Interview</h1>
        <a href="/" className="secondary-btn small">Home</a>
      </div>

      <section className="interview-panel">
        <span className="eyebrow">Question {currentIndex + 1}</span>
        <h2>{questions[currentIndex]}</h2>

        <textarea
          className="answer-box"
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Type your answer here..."
          rows={10}
        />

        <div className="cta-row">
          <button className="primary-btn" type="button" onClick={handleSubmit} disabled={isLoading || !answer.trim()}>
            {isLoading ? "Evaluating..." : "Submit Answer"}
          </button>
          <button className="secondary-btn" type="button" onClick={nextQuestion}>
            Next Question
          </button>
        </div>
      </section>

      {evaluation ? (
        <section className="panel">
          <h2>Evaluation</h2>
          <div className="metrics-grid" style={{ marginBottom: 8 }}>
            <div className="metric-card">
              <p>Overall</p>
              <strong>{evaluation.overall_score}%</strong>
            </div>
            <div className="metric-card">
              <p>Technical</p>
              <strong>{evaluation.technical_accuracy}%</strong>
            </div>
            <div className="metric-card">
              <p>Communication</p>
              <strong>{evaluation.communication}%</strong>
            </div>
            <div className="metric-card">
              <p>Problem Solving</p>
              <strong>{evaluation.problem_solving}%</strong>
            </div>
          </div>
          <p>{evaluation.feedback}</p>
          <p><strong>Improvement tip:</strong> {evaluation.improvement_tip}</p>
        </section>
      ) : null}

      <section className="panel">
        <h2>Question Bank</h2>
        <ul className="list compact">
          {questions.map((question, index) => (
            <li key={question + index}>{index + 1}. {question}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}

