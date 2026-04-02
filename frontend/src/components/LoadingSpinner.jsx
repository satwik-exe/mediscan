/**
 * LoadingSpinner.jsx
 * Displays an animated CSS spinner with a status message while
 * the PDF is being analyzed by the backend.
 */

import "./LoadingSpinner.css";

function LoadingSpinner() {
  return (
    <div className="spinner-container">
      <div className="spinner-ring" aria-hidden="true">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
      <p className="spinner-text">Analyzing your report…</p>
      <p className="spinner-subtext">This may take a few seconds</p>
    </div>
  );
}

export default LoadingSpinner;