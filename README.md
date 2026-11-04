# IEEE Research Paper Generator

AI-powered system that converts review literature into IEEE-compliant, publication-ready research papers using RAG and LaTeX automation.

## Project Structure

```
├── frontend/          # React + Vite frontend
├── backend/           # FastAPI backend
└── docs/             # Documentation
```

## Setup

### Supabase database

1. Create a Supabase project and enable the `vector` extension.
2. Open **SQL Editor** in Supabase and run the contents of `backend/schema.sql`.
3. Copy the project URL and API key from **Project Settings -> API**.

> `SUPABASE_URL` must be the Supabase HTTP(S) project URL (for example, `https://your-project.supabase.co`). Do not use a PostgreSQL connection string here; the application uses the Supabase Python client.

### Backend environment

From the repository root:

```bash
cd backend
cp .env.example .env
# Set SUPABASE_URL, SUPABASE_KEY and GEMINI_API_KEY in .env
pip install -r requirements.txt
python start.py
```

### Docker Compose

Create `backend/.env` using the steps above, then run from the repository root:

```bash
docker compose up --build
```

The Docker setup connects to the hosted Supabase project configured in `backend/.env`; it does not start a separate PostgreSQL container.

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend (alternative direct start)
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python main.py
```

## Tech Stack

- Frontend: React, Vite, Tailwind CSS
- Backend: FastAPI, LangChain, Gemini 3
- Database: Supabase (Postgres + pgvector)
- Formatting: LaTeX (IEEEtran)
