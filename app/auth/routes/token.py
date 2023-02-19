from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core import deps
from auth.serializers.token import RenewAccessTokenSerializer


router = APIRouter()

@router.post("/refresh-token/", response_model=RenewAccessTokenSerializer)
def renew_access_token(
    db: Session = Depends(deps.get_db),
    token_payload: dict = Depends(deps.get_decoded_token),
):
    pass
