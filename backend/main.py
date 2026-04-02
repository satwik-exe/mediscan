"""
main.py
-------
FastAPI application entry point for MediScan — Health Report Analyzer.
Single POST /analyze endpoint: accepts a PDF, extracts text,
runs Gemini analysis, returns structured JSON results.
"""

import google.generativeai as genai
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from analyzer import analyze_report
from parser import extract_text_from_pdf

app = FastAPI(
    title="MediScan API",
    description="Health lab report analyzer powered by Google Gemini",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Simple health check to confirm the API is running."""
    return {"status": "ok", "service": "MediScan API"}


@app.post("/analyze")
async def analyze_lab_report(file: UploadFile = File(...)):
    """
    Accept a PDF lab report and return structured analysis.

    Args:
        file: The uploaded PDF file (multipart/form-data).

    Returns:
        JSON with summary, lab values, flagged count, total count.

    Raises:
        HTTPException 400: File is not a PDF or no file provided.
        HTTPException 422: PDF cannot be parsed.
        HTTPException 500: LLM API call fails.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted. Please upload a .pdf file.",
        )

    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to read uploaded file: {str(e)}",
        )

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    try:
        extracted_text = extract_text_from_pdf(file_bytes)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Unexpected error while parsing PDF: {str(e)}",
        )

    try:
        analysis = analyze_report(extracted_text)
    except EnvironmentError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during analysis: {str(e)}",
        )

    values = analysis.get("values", [])
    flagged = [v for v in values if v.get("status", "normal") != "normal"]

    return {
        "success": True,
        "filename": file.filename,
        "summary": analysis.get("summary", ""),
        "values": values,
        "flagged_count": len(flagged),
        "total_count": len(values),
    }
```

---

### All other files are fine

`parser.py`, `reference_ranges.py`, and all frontend files don't use the API key — they don't need changes. Just make sure they only contain the code (no markdown text around it).

---

## Step 3 — Create your `.env` file

Inside `backend/`, create a new file called exactly `.env` (not `.env.example`) and put:
```
GEMINI_API_KEY=AIzaSyBh3nlb2AUkNqcyY6o8JhPhvKUucFodgKc