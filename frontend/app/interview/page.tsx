const questions = [
  "Tell me about a project that demonstrates your strongest technical skills.",
  "How would you scale a backend system that receives millions of requests per second?",
  "Walk me through a difficult bug you debugged and how you fixed it.",
  "Describe how you handle trade-offs between performance, cost, and reliability."
];

export default function InterviewPage() {
  return (
    <main className="page-shell inner-page">
      <div className="section-header">
        <h1>AI Mock Interview</h1>
        <a href="/" className="secondary-btn small">Home</a>
      </div>

      <section className="interview-panel">
        <span className="eyebrow">Current Question</span>
        <h2>{questions[1]}</h2>

        <textarea
          className="answer-box"
          placeholder="Type your answer here..."
          rows={10}
        />

        <div className="cta-row">
          <button className="primary-btn" type="button">Submit Answer</button>
          <button className="secondary-btn" type="button">Skip to Next</button>
        </div>
      </section>

      <section className="panel">
        <h2>Question Bank</h2>
        <ul className="list compact">
          {questions.map((question, index) => (
            <li key={question}>{index + 1}. {question}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}
