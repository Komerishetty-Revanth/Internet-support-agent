# Internet Support Agent

AI-powered internet troubleshooting assistant built with FastAPI and a simple web UI.

## Features

- Customer support chat workflow for internet issues
- Issue classification and troubleshooting stages
- Escalation support in conversation flow
- SQLite-backed persistence with SQLAlchemy
- Frontend served directly by FastAPI

## Project Structure

- `/app` - backend API, agent logic, services, and database models
- `/frontend` - static chat interface (HTML/CSS/JS)
- `/tests` - test suite

## Prerequisites

- Python 3.10+

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment variables and fill keys:

   ```bash
   cp .env.example .env
   ```

## Run

Start the app from the repository root:

```bash
python -m app.main
```

Then open `http://localhost:8000` in your browser.

## API Endpoints

- `POST /api/chat` - send a customer message to the support agent
- `GET /api/health` - chat route health check
- `GET /health` - app health check

## Tests

Run tests with:

```bash
pytest
```
