# LegalEase — AI-Powered Legal Document Generator

A Streamlit frontend + FastAPI backend + Gemini AI draft generator, with editable output and TXT/DOCX/PDF export.

> AI-generated drafts are not legal advice and may be incomplete or unsuitable for your jurisdiction. Have a qualified lawyer review before signing or relying on them. Avoid entering confidential personal data.

## Setup (Windows PowerShell)
Requires Python 3.10+ and a Gemini API key.
```powershell
cd "path\to\LegalEase"
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `.env` and set `GEMINI_API_KEY`. `GEMINI_MODEL` defaults to `gemini-2.5-flash`.

## Run in two VS Code terminals
Terminal 1:
```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
Terminal 2:
```powershell
streamlit run frontend/app.py
```
UI: http://localhost:8501 | API docs: http://127.0.0.1:8000/docs | Health: http://127.0.0.1:8000/api/health

## Test
```powershell
python -m pytest
```
Tests do not require Gemini. Live generation requires a valid key and model access.

## API
POST `/api/generate` accepts `document_type`, `parties`, `terms`, `effective_date`, optional `jurisdiction`, and `additional_instructions`. GET `/api/health` checks service readiness.

The attached project guide describes FastAPI + Streamlit + Gemini and TXT/DOCX/PDF. Its Gemini 1.5 Pro reference is dated; model is configurable. Confirm the selected model is available to your Google AI Studio key.
