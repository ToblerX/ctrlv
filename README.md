# Ctrl-V Game Card API + Telegram Bot

A free, self-contained API for generating game cards for the Ukrainian party game **"Ctrl V"** (inspired by the YouTube show [КтрлВе](https://www.youtube.com/watch?v=O5eSviXCWT0)).

The API returns a randomized **game mode**, a **topic prompt** in Ukrainian, and **3 secret Ukrainian nouns** that a player must weave into their improvisation. Includes a **Telegram bot** for playing directly in chat.

## Setup

### Option 1: Local (API only)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Option 2: Local (API + Bot)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload                    # terminal 1
BOT_TOKEN=your-token API_URL=http://127.0.0.1:8000 python -m bot.main  # terminal 2
```

### Option 3: Docker (API + Bot)

```bash
cp .env.example .env   # then edit .env and set your BOT_TOKEN
docker compose up --build
```

The API runs at `http://127.0.0.1:8000`.  
Interactive API docs are available at `http://127.0.0.1:8000/docs`.

## Telegram Bot

Create a bot via [@BotFather](https://t.me/BotFather), set the token in `.env`, and run via Docker.

**Bot commands:**

| Command | Description |
|---------|-------------|
| `/start` | Welcome message with available commands |
| `/card` | Generate a game card (shows mode selection buttons) |
| `/rules` | Show game rules in Ukrainian |

## API Usage

### `GET /api/v1/game-card`

Generate a random game card. Optionally pass a `mode` query parameter to lock a specific game mode.

**Random mode:**

```bash
curl http://127.0.0.1:8000/api/v1/game-card
```

**Specific mode:**

```bash
curl http://127.0.0.1:8000/api/v1/game-card?mode=monologue
```

**Response:**

```json
{
  "success": true,
  "data": {
    "mode": "monologue",
    "topic": "Тост колишньої на весіллі",
    "words": ["кадило", "блендер", "проспект"]
  }
}
```

**Invalid mode (422):**

```json
{
  "detail": [
    {
      "type": "enum",
      "msg": "Input should be 'random', 'monologue', 'teleshopping', 'debates' or 'miniature'"
    }
  ]
}
```

### `GET /api/v1/rules`

Returns the full game rules as markdown text.

```bash
curl http://127.0.0.1:8000/api/v1/rules
```

**Response:**

```json
{
  "success": true,
  "data": {
    "rules": "# Правила гри «Ctrl V»\n\n..."
  }
}
```

## Rate Limiting

All endpoints are rate-limited per IP address:

| Endpoint | Limit |
|----------|-------|
| `GET /api/v1/game-card` | 30 requests/minute |
| `GET /api/v1/rules` | 10 requests/minute |
| `GET /` | 60 requests/minute |

Exceeding the limit returns `429 Too Many Requests`:

```json
{
  "success": false,
  "error": "Rate limit exceeded. Try again later."
}
```

## Game Modes

| Mode | Key | Description |
|------|-----|-------------|
| Monologue | `monologue` | One player tells a story or gives a speech (1 min) |
| Teleshopping | `teleshopping` | One player pitches an everyday object like a TV infomercial (1 min) |
| Debates | `debates` | Two players argue opposing sides of a topic (2 min) |
| Miniature | `miniature` | Two players act out a scene together (1.5-2 min) |

## Project Structure

```
├── app/                         # FastAPI API
│   ├── main.py                  # App entry point, rate limiter
│   ├── routers/
│   │   ├── game_card.py         # GET /api/v1/game-card
│   │   └── rules.py             # GET /api/v1/rules
│   ├── services/
│   │   └── game_card_service.py # Randomization logic, GameMode enum
│   └── data/
│       ├── words.json           # 1000 Ukrainian nouns
│       └── topics.json          # 50 topics per game mode
├── bot/                         # Telegram bot (aiogram 3)
│   ├── main.py                  # Bot entry point
│   ├── api_client.py            # HTTP client to the API
│   ├── keyboards.py             # Inline mode selection keyboard
│   └── handlers/
│       └── commands.py          # /start, /card, /rules handlers
├── rules.md                     # Game rules in Ukrainian
├── Dockerfile                   # API container
├── bot.Dockerfile               # Bot container
├── docker-compose.yml           # API + bot services
└── .env.example                 # Environment variables template
```

## Server Deployment

### 1. Generate a deploy key on your server

```bash
ssh-keygen -t ed25519 -C "ctrlv-deploy" -f ~/.ssh/ctrlv_deploy
```

Press Enter twice (no passphrase needed for automated deploys).

### 2. Add the public key to GitHub

Copy the public key:

```bash
cat ~/.ssh/ctrlv_deploy.pub
```

Then go to your repo **Settings > Deploy keys > Add deploy key**, paste the key, and give it a title (e.g. "My Server"). Leave "Allow write access" unchecked (read-only is enough).

### 3. Configure SSH to use the deploy key

```bash
cat >> ~/.ssh/config << 'EOF'
Host github-ctrlv
    HostName github.com
    User git
    IdentityFile ~/.ssh/ctrlv_deploy
    IdentitiesOnly yes
EOF
```

### 4. Clone and run

```bash
git clone git@github-ctrlv:ToblerX/ctrlv.git
cd ctrlv
cp .env.example .env
nano .env   # set your BOT_TOKEN
docker compose up -d --build
```

### 5. Update the app

```bash
cd ctrlv
git pull
docker compose up -d --build
```

## License

See [LICENSE](LICENSE).
