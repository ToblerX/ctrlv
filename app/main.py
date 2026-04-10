from fastapi import FastAPI

from app.routers.game_card import router as game_card_router
from app.routers.rules import router as rules_router

app = FastAPI(
    title="Ctrl-V Game Card API",
    description="API for generating game cards for the Ukrainian party game 'Ctrl V' (КтрлВе).",
    version="1.0.0",
)

app.include_router(game_card_router)
app.include_router(rules_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "name": "Ctrl-V Game Card API",
        "version": "1.0.0",
        "docs": "/docs",
        "game_card_endpoint": "/api/v1/game-card",
    }
