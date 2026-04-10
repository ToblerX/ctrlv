from pathlib import Path

from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/api/v1", tags=["Rules"])

RULES_PATH = Path(__file__).resolve().parent.parent.parent / "rules.md"
RULES_TEXT = RULES_PATH.read_text(encoding="utf-8")


@router.get("/rules")
@limiter.limit("10/minute")
def rules(request: Request):
    return {"success": True, "data": {"rules": RULES_TEXT}}
