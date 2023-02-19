from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core import deps
from app.auth.serializers.token import (
    TokenReadSerializer,
    RenewAccessTokenSerializer
)
from app.core import deps
from app.core.security import renew_access_token


router = APIRouter()

@router.post("/refresh-token/")
async def refresh_access_token(
    access_token: RenewAccessTokenSerializer,
    db: Session = Depends(deps.get_db),
):
    return renew_access_token(
        db, token=access_token.token
    )

    # Check refresh token is valid
    # Get user_id
    # Call get access token method
    # Invalidate previous tokens on pre_create
    # Return new token n refresh token