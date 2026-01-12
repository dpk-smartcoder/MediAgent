# MediAgent

Multi-agent medical diagnosis platform that runs specialist AI agents (Cardiology, Psychology, Pulmonology) in parallel and fuses their findings into one comprehensive report.

## Table of Contents
- Overview
- Demo / Video
- Tech Stack
- Features
- Project Structure
- Getting Started
- Configuration
- Running the App
- API Routes

## Overview
MediAgent combines multiple domain-specific agents behind a Flask API and a React/Tailwind UI. Users upload or paste medical reports; agents analyze concurrently, and a multidisciplinary synthesizer returns a single Markdown-formatted diagnosis.

## Demo / Video
- Demo video: _Add link (YouTube/Drive)_
- Screenshots: _Add links/paths_

## Tech Stack
- Backend: Flask, LangChain, Google Gemini 2.5 Flash, Flask-CORS, python-dotenv
- Frontend: React 18, React Router DOM, Tailwind CSS, React Markdown, Fetch API
- Tooling: Python venv, npm, dotenv

## Features
- Parallel specialist agents + multidisciplinary synthesis
- File upload (.txt) or raw text input; Markdown output
- Responsive UI with loading/error states
- Env-driven configuration for API keys and endpoints

## Project Structure
```
MediAgent/
├── Backend/
│   └── model_and_api_multiagentic_diagnosis/
│       ├── app.py                    # Flask API server
│       ├── requirements.txt          # Python deps
│       ├── Utils/
│       │   └── Agents.py             # Agent classes
│       └── Medical Reports/          # Sample reports
├── Frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.js               # Upload page
│   │   │   └── Results.js            # Results page
│   │   ├── services/
│   │   │   └── api.js                # API calls
│   │   ├── App.js                    # Main app
│   │   └── index.js                  # Entry point
│   ├── package.json                  # Node deps
│   └── tailwind.config.js            # Tailwind config
└── README.md
```

## Getting Started
### Clone
```bash
git clone https://github.com/<your-org>/MediAgent.git
cd MediAgent
```

### Backend Setup
```bash
cd Backend/model_and_api_multiagentic_diagnosis
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd Frontend
npm install
```

## Configuration
Create `.env` in `Backend/model_and_api_multiagentic_diagnosis`:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

(Optional) `.env` in `Frontend`:
```env
REACT_APP_API_URL=http://localhost:5000
```

## Running the App
Backend (port 5000):
```bash
cd Backend/model_and_api_multiagentic_diagnosis
venv\Scripts\activate  # or source venv/bin/activate
python app.py
```

Frontend (port 3000):
```bash
cd Frontend
npm start
```

## API Routes
- `GET /` — Health check  
  Response: `{"status":"API is running","message":"Use POST /process_string (JSON body) or POST /process_file (File Upload) for analysis."}`

- `POST /process_file` — Analyze uploaded `.txt` report  
  Body: multipart/form-data with `file`  
  Response: `{"status":"success","diagnosis":"...","filename_processed":"report.txt"}`

- `POST /process_string` — Analyze raw text  
  Body: `{"report_content":"..."}`
  Response: `{"status":"success","diagnosis":"..."}`
