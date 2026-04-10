# Ctrl-V Game Card API

## What is this?
A self-contained FastAPI backend that generates randomized "Game Cards" for hosting the Ukrainian party game "Ctrl V" (inspired by the YouTube show "КтрлВе"). Each card contains a game mode, a Ukrainian-language topic prompt, and 3 random Ukrainian nouns.

## Tech Stack
- **Python 3.10+** with **FastAPI** and **Uvicorn**
- No database — all data lives in static JSON files under `app/data/`

## How to Run

**Locally:**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**With Docker:**
```bash
docker compose up --build
```

The server starts at `http://127.0.0.1:8000`. Swagger docs are at `/docs`.

## Project Structure
```
app/
├── main.py                  # FastAPI app entry point
├── routers/game_card.py     # GET /api/v1/game-card endpoint
├── services/game_card_service.py  # Randomization logic, data loading
└── data/
    ├── words.json           # 200+ Ukrainian nouns
    └── topics.json          # Topics grouped by game mode
```

## Key Conventions
- All game content (words, topics) is in Ukrainian
- API responses follow `{"success": bool, "data": {...}}` / `{"success": bool, "error": "..."}` format
- Data files are loaded once at module import time (no per-request I/O)
- Valid game modes: `monologue`, `teleshopping`, `debates`, `miniature`
