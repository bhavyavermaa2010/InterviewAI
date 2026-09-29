# InterviewAI

InterviewAI is an AI-powered interview preparation and evaluation platform that helps candidates improve their interview readiness using their resume, target job description, and mock interview simulations.

## Overview

This project combines:

- Next.js frontend for the user experience
- FastAPI backend for AI-powered analysis and interview APIs
- Ollama + LLaMA for local LLM inference
- PostgreSQL for interview history and user data

## Features

- Resume upload and parsing
- Job description analysis
- Skill gap matching between resume and JD
- Personalized interview question generation
- AI mock interview flow
- Scorecards and feedback dashboard
- Interview history tracking

## Architecture

- Frontend: Next.js
- Backend: FastAPI
- AI: Ollama + LLaMA 3
- Database: PostgreSQL
- Optional vector storage: pgvector / Qdrant for RAG

## Quick start

### 1. Install backend dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Start the backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/docs for Swagger UI.

### 3. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

### 4. Optional: Local LLM with Ollama

Install Ollama and run:

```bash
ollama pull llama3
```

Then set your environment file:

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

## Environment setup

Create a `.env` file in `backend/` with:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

For frontend, create `.env.local` in `frontend/` with:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project status

This repository includes a working starter app with real resume/job analysis logic, PDF extraction hooks, and AI-assisted interview evaluation. It is designed to act as the foundation for a production-grade interview training platform.

## Recommended next improvements

- Add PostgreSQL persistence for interviews and user profiles
- Add authentication and account management
- Add resume parsing from uploaded PDFs into structured fields
- Add vector-based semantic matching with pgvector or Qdrant
- Add multi-turn interview sessions with feedback history logs
