# Ctrl-V Game Card API

A free, self-contained API for generating game cards for the Ukrainian party game **"Ctrl V"** (inspired by the YouTube show [КтрлВе](https://www.youtube.com/watch?v=O5eSviXCWT0)).

The API returns a randomized **game mode**, a **topic prompt** in Ukrainian, and **3 secret Ukrainian nouns** that a player must weave into their improvisation.

## Setup

### Option 1: Local

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Option 2: Docker

```bash
docker compose up --build
```

The server runs at `http://127.0.0.1:8000`.  
Interactive API docs are available at `http://127.0.0.1:8000/docs`.

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

**Invalid mode (400):**

```json
{
  "success": false,
  "error": "Invalid mode 'foo'. Must be one of: monologue, teleshopping, debates, miniature"
}
```

## Game Modes

| Mode | Key | Description |
|------|-----|-------------|
| Monologue | `monologue` | One player tells a story or gives a speech (1 min) |
| Teleshopping | `teleshopping` | One player pitches an everyday object like a TV infomercial (1 min) |
| Debates | `debates` | Two players argue opposing sides of a topic (2 min) |
| Miniature | `miniature` | Two players act out a scene together (1.5-2 min) |

## License

See [LICENSE](LICENSE).
