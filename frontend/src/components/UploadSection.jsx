/**
 * UploadSection.jsx
 * File upload interface: drag-and-drop zone, file validation,
 * axios POST to /analyze, loading state, and error display.
 * Calls onAnalysisComplete(data) on success.
 */

import { useState, useRef } from "react";
import axios from "axios";
import LoadingSpinner from "./LoadingSpinner.jsx";
import "./UploadSection.css";

const API_URL = "http://localhost:8000/analyze";

function UploadSection({ onAnalysisComplete }) {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  function selectFile(chosen) {
    setError(null);
    if (!chosen) return;
    if (chosen.type !== "application/pdf" && !chosen.name.toLowerCase().endsWith(".pdf")) {
      setError("Only PDF files are accepted. Please select a .pdf file.");
      return;
    }
    setFile(chosen);
  }

  function handleDragOver(e) { e.preventDefault(); setIsDragging(true); }
  function handleDragLeave(e) { e.preventDefault(); setIsDragging(false); }

  function handleDrop(e) {
    e.preventDefault();
    setIsDragging(false);
    selectFile(e.dataTransfer.files[0]);
  }

  function handleInputChange(e) { selectFile(e.target.files[0]); }

  function handleClearFile() {
    setFile(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  async function handleAnalyze() {
    if (!file || isLoading) return;
    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(API_URL, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      onAnalysisComplete(response.data);
    } catch (err) {
      const detail =
        err.response?.data?.detail ||
        err.message ||
        "An unexpected error occurred. Please try again.";
      setError(detail);
    } finally {
      setIsLoading(false);
    }
  }

  if (isLoading) {
    return (
      <div className="upload-section">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="upload-section">
      <div className="upload-hero">
        <h1 className="upload-title">Understand Your Lab Results</h1>
        <p className="upload-subtitle">
          Upload a medical lab report PDF. MediScan will extract the values,
          flag anything outside normal ranges, and explain what it means — in
          plain English.
        </p>
      </div>

      <div
        className={`drop-zone ${isDragging ? "drop-zone--active" : ""} ${file ? "drop-zone--has-file" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !file && fileInputRef.current?.click()}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === "Enter" && !file && fileInputRef.current?.click()}
        aria-label="PDF upload area"
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleInputChange}
          style={{ display: "none" }}
        />

        {file ? (
          <div className="file-selected">
            <span className="file-icon">📄</span>
            <div className="file-info">
              <span className="file-name">{file.name}</span>
              <span className="file-size">{(file.size / 1024).toFixed(1)} KB</span>
            </div>
            <button
              className="btn-clear"
              onClick={(e) => { e.stopPropagation(); handleClearFile(); }}
              aria-label="Remove selected file"
            >✕</button>
          </div>
        ) : (
          <div className="drop-prompt">
            <span className="drop-icon">⤴</span>
            <p className="drop-primary">Drag & drop your PDF here</p>
            <p className="drop-secondary">or <span className="drop-link">browse to upload</span></p>
            <p className="drop-hint">PDF files only · Max 20 MB</p>
          </div>
        )}
      </div>

      {error && (
        <div className="error-banner" role="alert">
          <span className="error-icon">⚠</span>
          <span>{error}</span>
        </div>
      )}

      <button className="btn-analyze" onClick={handleAnalyze} disabled={!file}>
        Analyze Report
      </button>

      <div className="feature-pills">
        <span className="pill">⊕ Lab value extraction</span>
        <span className="pill">⊘ Abnormal flag detection</span>
        <span className="pill">⊙ Plain-English explanations</span>
      </div>
    </div>
  );
}

export default UploadSection;