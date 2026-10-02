import json

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from Backend.ai.fallback import (
    home_recommendation,
    jewelry_recommendation,
    party_recommendation,
)
from Backend.ai.gemini import get_gemini_recommendation
from Backend.database.db import save_recommendation
from Backend.security import decode_token


router = APIRouter(prefix="/planner", tags=["Planner"])


class PlannerRequest(BaseModel):
    planner: str
    data: dict


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


@router.post("/recommend")
def create_recommendation(
    request: PlannerRequest,
    user_id: int = Depends(get_current_user)
):
    planner = request.planner.strip().lower()

    if planner not in ["home", "party", "jewelry"]:
        raise HTTPException(
            status_code=400,
            detail="Planner must be Home, Party, or Jewelry."
        )

    gemini_result = get_gemini_recommendation(
        request.planner,
        request.data
    )

    if gemini_result:
        result = gemini_result
    else:
        if planner == "home":
            result = home_recommendation(request.data)

        elif planner == "party":
            result = party_recommendation(request.data)

        else:
            result = jewelry_recommendation(request.data)

    save_recommendation(
        user_id=user_id,
        planner=request.planner,
        request_data=json.dumps(request.data),
        response_data=json.dumps(result)
    )

    return result