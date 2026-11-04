# IEEE Research Paper Generator

An AI-assisted research paper workspace built with React, Vite, FastAPI, Supabase, Gemini, retrieval-augmented generation (RAG), and LaTeX export.

> **Important:** This application has two separate processes. Start the backend first, then start the frontend in a second terminal. Opening the repository README in a browser does not start the application.

## Project structure

```text
my-project/
├── frontend/              # React + Vite application
├── backend/               # FastAPI API and AI services
│   ├── .env.example       # Environment variable template
│   ├── schema.sql         # Supabase database schema
│   └── requirements.txt   # Python dependencies
├── docker/                # Docker configuration
├── Dockerfile.backend
├── Dockerfile.frontend
└── docker-compose.yml
```

## Requirements

- Windows 10/11
- Python 3.10 or 3.11 (Python 3.11 recommended)
- Node.js 18 or newer (includes npm)
- A Supabase project
- A Gemini API key

Check the installations in the VS Code terminal:

```powershell
py --version
node --version
npm --version
```

## 1. Get the project

If you have not cloned the repository:

```powershell
git clone https://github.com/sethumadhavan505/my-project.git
cd my-project
git fetch origin
git checkout fix/backend-database-critical
```

If you already cloned it:

```powershell
git fetch origin
git checkout fix/backend-database-critical
git pull origin fix/backend-database-critical
```

## 2. Configure Supabase

1. Open your project in the Supabase dashboard.
2. Open **SQL Editor** and create a new query.
3. Copy all of `backend/schema.sql` into the editor and run it.
4. Open **Project Settings → API** and copy the project URL and an appropriate API key.

The `SUPABASE_URL` value must be the HTTPS project URL (for example, `https://your-project.supabase.co`), not a PostgreSQL connection string.

## 3. Configure backend environment variables

In VS Code, open the `backend` folder and create a file named `.env` by copying `.env.example`. Put your own current credentials in it:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit or share this file. The repository `.gitignore` excludes `.env`. Never put a Supabase secret/service-role key or Gemini key in frontend code.

## 4. Start the backend (Terminal 1)

From the repository root in PowerShell:

```powershell
cd backend
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python start.py
```

If PowerShell blocks virtual-environment activation, run this once in that terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

The backend should report that it is serving at:

- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs

Keep Terminal 1 open. The first installation can take several minutes because the embedding-model dependencies are large.

## 5. Start the frontend (Terminal 2)

In VS Code choose **Terminal → New Terminal**. From the repository root run:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite. The configured development port is:

**http://localhost:3000**

Keep Terminal 2 open as well. Use the application at this address, not the GitHub repository page or the README preview.

## 6. Check the services

Open these URLs:

- http://localhost:8000/ — backend health response
- http://localhost:8000/docs — backend API documentation
- http://localhost:3000/ — React application

The frontend uses the backend at `http://localhost:8000` by default. Do not expose API keys through Vite `VITE_*` variables.

## Troubleshooting

| Problem | What to do |
|---|---|
| `py` is not recognized | Install Python 3.11 and enable **Add Python to PATH**, then reopen VS Code. |
| `npm` is not recognized | Install Node.js 18+ and reopen VS Code. |
| `ModuleNotFoundError` | Activate the backend virtual environment and rerun `python -m pip install -r requirements.txt`. |
| Missing environment variables | Confirm the file is named exactly `backend/.env` and contains all three values. |
| Supabase table or relation error | Run the complete `backend/schema.sql` in the correct Supabase project. |
| Port 8000 is already in use | Stop the other process using port 8000, then restart the backend. |
| Frontend says backend disconnected | Keep the backend terminal running and check http://localhost:8000/. |

## Docker

Docker Compose is an alternative to the two-terminal local setup. Create `backend/.env` first, then from the repository root run:

```powershell
docker compose up --build
```

The Docker backend uses the hosted Supabase project configured in `backend/.env`; it does not require a separate local PostgreSQL service.

## Technology

- Frontend: React 18, Vite, Tailwind CSS
- Backend: FastAPI, Python
- Database: Supabase PostgreSQL with pgvector
- AI: Gemini and sentence-transformers embeddings
- Document processing: PDF and DOCX
- Export: LaTeX / IEEE-style formatting
