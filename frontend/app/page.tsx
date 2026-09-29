const featureCards = [
  {
    title: "Resume Analysis",
    description: "Upload a resume, extract skills, and identify strengths and gaps.",
  },
  {
    title: "JD Matching",
    description: "Compare the resume against the target job description and highlight missing skills.",
  },
  {
    title: "AI Mock Interviews",
    description: "Practice with adaptive, job-specific questions and personalized evaluation.",
  },
  {
    title: "Performance Dashboard",
    description: "Track scores, progress, weak areas, and interview history over time.",
  },
];

export default function HomePage() {
  return (
    <main className="page-shell">
      <section className="hero">
        <nav className="topbar">
          <div className="brand">InterviewAI</div>
          <div className="nav-links">
            <a href="#features">Features</a>
            <a href="/dashboard">Dashboard</a>
            <a href="/interview">Practice</a>
          </div>
        </nav>

        <div className="hero-content">
          <div>
            <span className="eyebrow">AI Interview Preparation</span>
            <h1>Prepare for the role you want with intelligent, personalized practice.</h1>
            <p>
              Upload your resume, match against a job description, and rehearse with AI-powered mock interviews that evaluate your answers in real time.
            </p>
            <div className="cta-row">
              <a className="primary-btn" href="/dashboard">View Dashboard</a>
              <a className="secondary-btn" href="/interview">Start Mock Interview</a>
            </div>
          </div>

          <div className="score-panel">
            <p className="mini-label">Performance Snapshot</p>
            <div className="score-item">
              <span>Technical</span>
              <strong>78%</strong>
            </div>
            <div className="score-item">
              <span>Communication</span>
              <strong>82%</strong>
            </div>
            <div className="score-item">
              <span>Problem Solving</span>
              <strong>71%</strong>
            </div>
            <div className="score-item">
              <span>Projects</span>
              <strong>85%</strong>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className="features">
        <h2>Core Features</h2>
        <div className="feature-grid">
          {featureCards.map((feature) => (
            <article key={feature.title} className="feature-card">
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
