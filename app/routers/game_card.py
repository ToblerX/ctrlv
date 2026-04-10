from fastapi import APIRouter, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.services.game_card_service import GameMode, get_random_game_card

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/api/v1", tags=["Game Card"])


@router.get("/game-card")
@limiter.limit("30/minute")
def game_card(request: Request, mode: GameMode = Query(default=GameMode.random)):
    data = get_random_game_card(mode)
    return {"success": True, "data": data}
