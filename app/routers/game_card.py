from fastapi import APIRouter, Query

from app.services.game_card_service import GameMode, get_random_game_card

router = APIRouter(prefix="/api/v1", tags=["Game Card"])


@router.get("/game-card")
def game_card(mode: GameMode = Query(default=GameMode.random)):
    data = get_random_game_card(mode)
    return {"success": True, "data": data}
