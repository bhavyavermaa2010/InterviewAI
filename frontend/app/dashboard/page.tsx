export default function DashboardPage() {
  const metrics = [
    { label: "Overall Performance", value: "79%" },
    { label: "Technical", value: "78%" },
    { label: "Communication", value: "82%" },
    { label: "Problem Solving", value: "71%" },
  ];

  const areas = ["DBMS", "System Design", "Project Explanation"];

  return (
    <main className="page-shell inner-page">
      <div className="section-header">
        <h1>Interview Performance Dashboard</h1>
        <a href="/" className="secondary-btn small">Back Home</a>
      </div>

      <div className="metrics-grid">
        {metrics.map((item) => (
          <div key={item.label} className="metric-card">
            <p>{item.label}</p>
            <strong>{item.value}</strong>
          </div>
        ))}
      </div>

      <div className="two-column">
        <section className="panel">
          <h2>Areas to Improve</h2>
          <ul className="list">
            {areas.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </section>

        <section className="panel">
          <h2>Recent Interview History</h2>
          <ul className="list compact">
            <li>System Design Mock Interview — 78%</li>
            <li>Resume-to-Job Match Review — 84%</li>
            <li>Behavioral Interview Session — 88%</li>
          </ul>
        </section>
      </div>
    </main>
  );
}
