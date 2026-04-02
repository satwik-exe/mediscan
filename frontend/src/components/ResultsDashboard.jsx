/**
 * ResultsDashboard.jsx
 * Displays the full analysis results after a lab report is processed.
 * Shows: summary card, stats (total/flagged/normal), flagged values
 * section, normal values section, and a reset button.
 */

import LabValueCard from "./LabValueCard.jsx";
import "./ResultsDashboard.css";

function ResultsDashboard({ results, onReset }) {
  const { filename, summary, values, flagged_count, total_count } = results;

  const flagged = values.filter((v) => v.status !== "normal");
  const normal = values.filter((v) => v.status === "normal");

  return (
    <div className="results-dashboard">
      <div className="results-header">
        <div>
          <h2 className="results-title">Analysis Complete</h2>
          <p className="results-filename">📄 {filename}</p>
        </div>
        <button className="btn-reset" onClick={onReset}>← Analyze Another</button>
      </div>

      <div className="summary-card">
        <h3 className="summary-label">Overall Summary</h3>
        <p className="summary-text">{summary}</p>
      </div>

      <div className="stats-row">
        <div className="stat-pill">
          <span className="stat-num">{total_count}</span>
          <span className="stat-label">Values Analyzed</span>
        </div>
        <div className={`stat-pill ${flagged_count > 0 ? "stat-pill--flagged" : ""}`}>
          <span className="stat-num">{flagged_count}</span>
          <span className="stat-label">Flagged</span>
        </div>
        <div className="stat-pill stat-pill--ok">
          <span className="stat-num">{total_count - flagged_count}</span>
          <span className="stat-label">Normal</span>
        </div>
      </div>

      {flagged.length > 0 && (
        <section className="values-section">
          <h3 className="section-title section-title--flagged">
            <span>⚠ Flagged Values</span>
            <span className="section-count">{flagged.length}</span>
          </h3>
          <div className="values-grid">
            {flagged.map((v, i) => <LabValueCard key={i} {...v} />)}
          </div>
        </section>
      )}

      {normal.length > 0 && (
        <section className="values-section">
          <h3 className="section-title">
            <span>✓ Normal Values</span>
            <span className="section-count">{normal.length}</span>
          </h3>
          <div className="values-grid">
            {normal.map((v, i) => <LabValueCard key={i} {...v} />)}
          </div>
        </section>
      )}

      {values.length === 0 && (
        <div className="empty-state">
          <p className="empty-icon">🔬</p>
          <p className="empty-text">No lab values were detected in this report.</p>
          <p className="empty-sub">The PDF may be a scanned image or use an uncommon format.</p>
          <button className="btn-reset" onClick={onReset}>Try Another File</button>
        </div>
      )}

      <div className="results-disclaimer">
        <strong>Reminder:</strong> This analysis is AI-generated and for informational
        purposes only. Always consult a qualified healthcare professional to interpret
        your results.
      </div>
    </div>
  );
}

export default ResultsDashboard;