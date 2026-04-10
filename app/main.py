from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.routers.game_card import router as game_card_router
from app.routers.rules import router as rules_router

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Ctrl-V Game Card API",
    description="API for generating game cards for the Ukrainian party game 'Ctrl V' (КтрлВе).",
    version="1.0.0",
)

app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"success": False, "error": "Rate limit exceeded. Try again later."},
    )


app.include_router(game_card_router)
app.include_router(rules_router)


@app.get("/", tags=["Root"])
@limiter.limit("60/minute")
def root(request: Request):
    return {
        "name": "Ctrl-V Game Card API",
        "version": "1.0.0",
        "docs": "/docs",
        "game_card_endpoint": "/api/v1/game-card",
    }
