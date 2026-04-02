# MediScan — Health Report Analyzer

An AI-powered web application that analyzes medical lab report PDFs, flags abnormal values against standard reference ranges, and generates plain-English explanations for non-medical users.

Built as a portfolio project demonstrating full-stack development with LLM integration in the healthcare domain.

---

## Features

- **PDF Upload** — Drag-and-drop or click-to-browse PDF upload
- **Lab Value Extraction** — Parses structured tables and raw text from lab reports
- **Reference Range Flagging** — Compares 26+ common lab values against standard ranges (Mayo Clinic / WHO)
- **AI Explanations** — Uses Claude to generate 2–3 sentence plain-English explanations for abnormal values
- **Clean Dashboard** — Color-coded status cards (normal / high / low / critical)
- **Overall Summary** — A 3–4 sentence AI-generated health snapshot

---

## Tech Stack

| Layer     | Technology                         |
|-----------|-------------------------------------|
| Frontend  | React 18 (Vite), plain CSS          |
| Backend   | Python 3.11+, FastAPI               |
| PDF Parse | pdfplumber                          |
| AI / LLM  | Anthropic Claude (claude-sonnet-4-20250514) |
| HTTP      | axios (frontend), httpx (backend)   |
| Auth      | Environment variable (no database)  |

---

## Project Structure

```
mediscan/
├── backend/
│   ├── main.py               # FastAPI app + /analyze endpoint
│   ├── parser.py             # PDF text extraction (pdfplumber)
│   ├── analyzer.py           # Claude API integration
│   ├── reference_ranges.py   # Standard lab reference ranges
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── UploadSection.jsx
│   │   │   ├── ResultsDashboard.jsx
│   │   │   ├── LabValueCard.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── .gitignore
└── README.md
```

---

## Setup — Backend

### Prerequisites
- Python 3.11 or higher
- An [Anthropic API key](#get-an-anthropic-api-key)

### Steps

```bash
cd mediscan/backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Open .env and set: ANTHROPIC_API_KEY=sk-ant-...

# Start the server
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.  
Swagger docs: `http://localhost:8000/docs`

---

## Setup — Frontend

### Prerequisites
- Node.js 18 or higher

### Steps

```bash
cd mediscan/frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The app will open at `http://localhost:5173`.

> The frontend expects the backend to be running at `http://localhost:8000`.

---

## Get an Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign in or create an account
3. Navigate to **API Keys** → **Create Key**
4. Copy the key and paste it into `backend/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

---

## Usage

1. Start the backend (`uvicorn main:app --reload --port 8000`)
2. Start the frontend (`npm run dev`)
3. Open `http://localhost:5173` in your browser
4. Upload a medical lab report PDF
5. Click **Analyze Report**
6. Review the results dashboard

---

## Notes & Limitations

- **Not a medical device.** Results are AI-generated and should not replace professional medical advice.
- **Text-based PDFs only.** Scanned image PDFs (without OCR text) cannot be parsed in v1.
- **Stateless.** No data is stored — each analysis is ephemeral.
- **Reference ranges** are based on commonly published adult reference values and may differ from your lab's specific ranges.

---

## Screenshots

*(coming soon)*

---

## Built with

> Built as a portfolio project demonstrating full-stack development with LLM integration in the healthcare domain.

- [FastAPI](https://fastapi.tiangolo.com/)
- [Anthropic Claude](https://www.anthropic.com/)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [React](https://react.dev/) + [Vite](https://vitejs.dev/)