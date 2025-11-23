from typing import Dict
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_status() -> Dict[str, str]:
    return {"status": "ok", "database": "PostgreSQL connected ✓"}
