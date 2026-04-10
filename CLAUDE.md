# Ctrl-V Game Card API + Telegram Bot

## What is this?
A self-contained FastAPI backend that generates randomized "Game Cards" for hosting the Ukrainian party game "Ctrl V" (inspired by the YouTube show "КтрлВе"). Each card contains a game mode, a Ukrainian-language topic prompt, and 3 random Ukrainian nouns. Includes a Telegram bot for playing directly in chat.

## Tech Stack
- **Python 3.12** with **FastAPI** and **Uvicorn** (API)
- **aiogram 3** with **aiohttp** (Telegram bot)
- **slowapi** for rate limiting
- No database — all data lives in static JSON files under `app/data/`

## How to Run

**Locally (API only):**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Locally (bot):**
```bash
BOT_TOKEN=your-token API_URL=http://127.0.0.1:8000 python -m bot.main
```

**With Docker (API + bot):**
```bash
cp .env.example .env   # then set BOT_TOKEN
docker compose up --build
```

The API starts at `http://127.0.0.1:8000`. Swagger docs are at `/docs`.

## Project Structure
```
├── app/                             # FastAPI API
│   ├── main.py                      # App entry point, rate limiter setup
│   ├── routers/
│   │   ├── game_card.py             # GET /api/v1/game-card
│   │   └── rules.py                 # GET /api/v1/rules
│   ├── services/
│   │   └── game_card_service.py     # Randomization logic, data loading, GameMode enum
│   └── data/
│       ├── words.json               # 1000 Ukrainian nouns
│       └── topics.json              # 50 topics per game mode
├── bot/                             # Telegram bot (aiogram 3)
│   ├── main.py                      # Bot entry point, polling
│   ├── api_client.py                # HTTP client to call the API
│   ├── keyboards.py                 # Inline keyboard for mode selection
│   └── handlers/
│       └── commands.py              # /start, /card, /rules handlers
├── rules.md                         # Game rules in Ukrainian (served by /api/v1/rules)
├── Dockerfile                       # Docker image for the API
├── bot.Dockerfile                   # Docker image for the bot
├── docker-compose.yml               # API + bot services
├── .env.example                     # Template for BOT_TOKEN and API_URL
└── requirements.txt                 # Python dependencies
```

## Key Conventions
- All game content (words, topics) is in Ukrainian
- API responses follow `{"success": bool, "data": {...}}` / `{"success": bool, "error": "..."}` format
- Data files are loaded once at module import time (no per-request I/O)
- Valid game modes: `monologue`, `teleshopping`, `debates`, `miniature`
- Rate limits: 30/min on game-card, 10/min on rules, 60/min on root
- Bot communicates with API over HTTP (separate service in Docker)
- Bot token is loaded from `BOT_TOKEN` env var
