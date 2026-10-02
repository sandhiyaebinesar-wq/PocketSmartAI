from fastapi import APIRouter, Depends, Header, HTTPException

from Backend.database.db import get_history
from Backend.security import decode_token


router = APIRouter(prefix="/history", tags=["History"])


def get_current_user(
    authorization: str | None = Header(default=None)
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Login required."
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format."
        )

    token = authorization.replace("Bearer ", "", 1).strip()

    try:
        return decode_token(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )


@router.get("/")
def get_user_history(
    user_id: int = Depends(get_current_user)
):
    rows = get_history(user_id)

    history = []

    for row in rows:
        history.append({
            "id": row["id"],
            "planner": row["planner"],
            "request_data": row["request_data"],
            "response_data": row["response_data"],
            "created_at": row["created_at"]
        })

    return {
        "history": history
    }
