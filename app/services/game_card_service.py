import json
import random
from enum import Enum
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "words.json", encoding="utf-8") as f:
    WORDS: list[str] = json.load(f)

with open(DATA_DIR / "topics.json", encoding="utf-8") as f:
    TOPICS: dict[str, list[str]] = json.load(f)


class GameMode(str, Enum):
    random = "random"
    monologue = "monologue"
    teleshopping = "teleshopping"
    debates = "debates"
    miniature = "miniature"


PLAYABLE_MODES = [m for m in GameMode if m != GameMode.random]


def get_random_game_card(mode: GameMode = GameMode.random) -> dict:
    if mode == GameMode.random:
        mode = random.choice(PLAYABLE_MODES)

    topic = random.choice(TOPICS[mode.value])
    words = random.sample(WORDS, 3)

    return {
        "mode": mode.value,
        "topic": topic,
        "words": words,
    }
