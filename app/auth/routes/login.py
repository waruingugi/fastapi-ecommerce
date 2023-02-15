from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.users.daos.user import user_dao
from app.exceptions.custom import IncorrectCredentials

from app.core.deps import get_db
from app.auth.serializers.token import TokenBaseSerializer

router = APIRouter()


@router.post("/access-token", response_model=TokenBaseSerializer)
async def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = user_dao.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )

    if not user:
        raise IncorrectCredentials

    access_token = create_access_token(
        data={"sub": user.phone, "scopes": form_data.scopes},
    )

    return {"access_token": access_token, "token_type": "bearer"}
