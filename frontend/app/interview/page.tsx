"use client";

import { ChangeEvent, useState } from "react";

type AnalysisResult = {
  candidate_summary: {
    strengths: string[];
    areas_to_improve: string[];
  };
  extracted_skills: string[];
  missing_skills: string[];
  match_score: number;
};

const defaultResume = `Senior software engineer with 5+ years of experience in backend systems, APIs, and cloud architecture.
Built scalable services using Python, FastAPI, PostgreSQL, Docker, and AWS.
Led a team of 3 engineers and improved system reliability by 30%.
`;

const defaultJobDescription = `We are hiring a backend engineer to design scalable APIs, optimize databases, and build cloud-native systems.
Requirements: Python, FastAPI, SQL, AWS, system design, microservices, distributed systems.`;

export default function DashboardPage() {
  const [resumeText, setResumeText] = useState(defaultResume);
  const [jobDescription, setJobDescription] = useState(defaultJobDescription);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    setIsLoading(true);
    setError("");

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
      const response = await fetch(`${apiUrl}/api/resume/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription }),
      });

      if (!response.ok) {
        throw new Error("Unable to analyze resume and job description.");
      }

      const data: AnalysisResult = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleResumeUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (file.type === "application/pdf") {
      setResumeText(
        "PDF upload received. This starter version uses text-based resume input for analysis. Connect pypdf or a PDF extraction library in production."
      );
      return;
    }

    const text = await file.text();
    setResumeText(text);
  };

  return (
    <main className="page-shell inner-page">
      <div className="section-header">
        <h1>Resume-to-Job Match</h1>
        <a href="/" className="secondary-btn small">Back Home</a>
      </div>

      <div className="two-column">
        <section className="panel">
          <h2>Resume Analysis</h2>

          <div style={{ marginBottom: 14 }}>
            <input type="file" accept=".txt,.pdf" onChange={handleResumeUpload} />
          </div>

          <textarea
            className="answer-box"
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
            rows={10}
            placeholder="Paste your resume text here..."
          />

          <h2 style={{ marginTop: 22 }}>Job Description</h2>
          <textarea
            className="answer-box"
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={8}
            placeholder="Paste the target job description here..."
          />

          <div className="cta-row">
            <button className="primary-btn" type="button" onClick={handleAnalyze} disabled={isLoading}>
              {isLoading ? "Analyzing..." : "Analyze Match"}
            </button>
          </div>

          {error ? <p style={{ color: "#ff9aa2", marginTop: 16 }}>{error}</p> : null}
        </section>

        <section className="panel">
          <h2>Match Summary</h2>

          {result ? (
            <>
              <div className="metric-card" style={{ marginBottom: 16 }}>
                <p>Overall Match Score</p>
                <strong>{result.match_score}%</strong>
              </div>

              <div style={{ marginBottom: 18 }}>
                <h3>Extracted Skills</h3>
                <ul className="list compact">
                  {result.extracted_skills.length ? (
                    result.extracted_skills.map((skill) => <li key={skill}>{skill}</li>)
                  ) : (
                    <li>No matching skills detected.</li>
                  )}
                </ul>
              </div>

              <div style={{ marginBottom: 18 }}>
                <h3>Missing Skills</h3>
                <ul className="list compact">
                  {result.missing_skills.length ? (
                    result.missing_skills.map((skill) => <li key={skill}>{skill}</li>)
                  ) : (
                    <li>No major skill gaps found.</li>
                  )}
                </ul>
              </div>

              <div>
                <h3>Strengths</h3>
                <ul className="list compact">
                  {result.candidate_summary.strengths.map((item) => <li key={item}>{item}</li>)}
                </ul>
              </div>

              <div style={{ marginTop: 18 }}>
                <h3>Areas to Improve</h3>
                <ul className="list compact">
                  {result.candidate_summary.areas_to_improve.map((item) => <li key={item}>{item}</li>)}
                </ul>
              </div>
            </>
          ) : (
            <p className="list">Upload a resume and job description to generate a match analysis.</p>
          )}
        </section>
      </div>
    </main>
  );
}

