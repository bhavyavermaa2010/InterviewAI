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
- Optional vector storage: pgvector / Qdrant for semantic matching

## Getting started

### 1. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/docs for Swagger UI.

### 3. With Docker Compose

```bash
docker compose up --build
```

## Environment variables

Create `.env` files as needed with:

- `NEXT_PUBLIC_API_URL=http://localhost:8000`
- `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/interviewai`
- `OLLAMA_BASE_URL=http://localhost:11434`

## Project status

This repository is a starter scaffold for the InterviewAI product. It includes a working frontend shell and a functional FastAPI backend foundation for the core interview features.
