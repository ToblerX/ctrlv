from pathlib import Path

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["Rules"])

RULES_PATH = Path(__file__).resolve().parent.parent.parent / "rules.md"
RULES_TEXT = RULES_PATH.read_text(encoding="utf-8")


@router.get("/rules")
def rules():
    return {"success": True, "data": {"rules": RULES_TEXT}}
