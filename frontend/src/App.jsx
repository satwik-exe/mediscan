/**
 * App.jsx
 * Root component for MediScan.
 * Manages top-level view state: "upload" or "results".
 * Passes data and handlers down to child components via props.
 */

import { useState } from "react";
import UploadSection from "./components/UploadSection.jsx";
import ResultsDashboard from "./components/ResultsDashboard.jsx";
import "./App.css";

function App() {
  const [view, setView] = useState("upload");
  const [results, setResults] = useState(null);

  function handleAnalysisComplete(data) {
    setResults(data);
    setView("results");
  }

  function handleReset() {
    setResults(null);
    setView("upload");
  }

  return (
    <div className="app-root">
      <header className="app-header">
        <div className="header-inner">
          <div className="logo">
            <span className="logo-icon">⊕</span>
            <span className="logo-name">MediScan</span>
          </div>
          <span className="logo-tagline">Health Report Analyzer</span>
        </div>
      </header>

      <main className="app-main">
        {view === "upload" ? (
          <UploadSection onAnalysisComplete={handleAnalysisComplete} />
        ) : (
          <ResultsDashboard results={results} onReset={handleReset} />
        )}
      </main>

      <footer className="app-footer">
        <p>
          MediScan is for informational purposes only. It is not a substitute
          for professional medical advice, diagnosis, or treatment.
        </p>
      </footer>
    </div>
  );
}

export default App;