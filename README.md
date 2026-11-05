# IEEE Research Paper Generator

An AI-assisted research-paper workflow with a React/Vite frontend and FastAPI backend. It stores papers and document embeddings in Supabase (Postgres with pgvector), extracts text from PDF/DOCX references, uses Gemini for section drafts, and exports IEEE-style LaTeX and PDF.

## Architecture

- `frontend/`: React 18 application and Vite development server.
- `backend/`: FastAPI routes, Supabase client, upload processing, embeddings, Gemini generation, and LaTeX export.
- `backend/schema.sql`: Supabase tables, pgvector setup, and similarity-search RPC.
- `docker-compose.yml`: production-style Docker deployment; the database remains in Supabase.

## Prerequisites

- Python 3.11 or later.
- Node.js 18 or later and npm.
- A Supabase project with the `vector` extension available.
- A Gemini API key.
- A LaTeX distribution with `pdflatex` for PDF export. The backend Docker image installs TeX Live.

## Supabase setup

1. Create a Supabase project and open its SQL Editor.
2. Run `backend/schema.sql`. It creates the required tables, pgvector index, and `match_documents` function. The file also includes additive `IF NOT EXISTS` statements for upload-processing status fields, so it can be re-run against an earlier version without deleting rows.
3. Keep the Supabase server-side key in the backend environment only. Never put it in a `VITE_*` variable or commit it to source control.
4. Copy the project URL (the HTTPS API URL, not a PostgreSQL connection string) and the server-side key into `backend/.env`.

The backend uses the Supabase REST client. It does not create a local Postgres database.

## Local development

### Backend

PowerShell:

```powershell
cd backend
Copy-Item .env.example .env
# Edit .env and set SUPABASE_URL, SUPABASE_KEY, and GEMINI_API_KEY.
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python start.py
```

The API is available at `http://localhost:8000`; interactive API documentation is at `http://localhost:8000/docs`. `GEMINI_MODEL` defaults to `gemini-3.6-flash` and can be changed to another model enabled for your Gemini API key. `CORS_ORIGINS` is a comma-separated list of browser origins; its local defaults allow the Vite development ports.

### Frontend

In another terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Open the Vite URL shown in the terminal (normally `http://localhost:3000`). Set `VITE_API_BASE_URL` in `frontend/.env` if the API is not at `http://localhost:8000`. Only public frontend settings belong in `VITE_*` variables; these values are embedded in the browser build.

## Docker deployment

1. Create `backend/.env` from `backend/.env.example` and set valid Supabase and Gemini credentials.
2. In a root `.env` file or the deployment environment, set:
   - `VITE_API_BASE_URL` to the backend URL reachable by users' browsers (for a local deployment, `http://localhost:8000`).
   - `CORS_ORIGINS` to the exact frontend origin(s), comma-separated (for a local deployment, `http://localhost:3000`).
3. From the repository root, build and start the application:

```powershell
docker compose up --build -d
docker compose logs -f
```

The frontend URL is `http://localhost:3000` and the API is `http://localhost:8000` for a local deployment. The Compose setup persists uploads and the embedding-model cache in named volumes. For a hosted deployment, configure HTTPS and use the public API origin in `VITE_API_BASE_URL` at build time and the frontend origin in `CORS_ORIGINS`. Rebuild the frontend after changing its `VITE_*` settings.

The development Compose variant is available with:

```powershell
docker compose -f docker-compose.dev.yml up --build
```

## API workflow

The frontend uses these main routes:

- `GET /`, `GET /api/system/status`: API, Supabase, embedding-model, and LaTeX readiness.
- `GET/POST /api/papers` and `GET /api/papers/{paper_id}`: list, create, and read papers.
- `GET /api/papers/{paper_id}/files` and `POST /api/papers/{paper_id}/upload`: list and upload PDF/DOCX reference files.
- `GET /api/papers/{paper_id}/processing-status`: file indexing and paper-generation progress.
- `GET/POST /api/papers/{paper_id}/sections` and `POST /api/generate`: read/save sections and generate a section using retrieved document context.
- `POST /api/papers/{paper_id}/generate-complete`, `POST /api/papers/{paper_id}/resume-generation`, and `GET /api/papers/{paper_id}/generation-status`: background full-paper generation and status.
- `GET /api/papers/{paper_id}/export`, `/export/latex`, and `/export/pdf`: text, IEEE-style LaTeX, and PDF exports.
- `GET /api/papers/{paper_id}/metrics`, `GET /api/latex/status`: paper metrics and PDF-export readiness.

Reference processing failures are reported in `processing-status`; a failed file is not treated as successfully indexed. Generated text must not be treated as verified scholarship: check every claim and citation, and add real source references before submission. The exporter does not invent bibliography entries.

## Tests and troubleshooting

- Backend syntax: `python -m compileall backend`
- Frontend production build: `cd frontend; npm ci; npm run build`
- API health: `GET http://localhost:8000/api/system/status`; `database_status` should be `connected`.
- Supabase connectivity or schema errors: verify `SUPABASE_URL`, the server-side `SUPABASE_KEY`, and that `backend/schema.sql` has been run.
- Gemini errors: verify `GEMINI_API_KEY`, `GEMINI_MODEL`, and model access for the key.
- PDF export errors: check `GET /api/latex/status` and ensure `pdflatex` and the IEEEtran LaTeX class are installed.
- Upload errors: confirm the selected file is a readable PDF/DOCX under the configured `MAX_FILE_SIZE`; inspect the API response or backend logs for indexing errors.

Do not commit `.env` files. If a credential was ever committed or shared, revoke/rotate it with its provider and update the private deployment environment.
