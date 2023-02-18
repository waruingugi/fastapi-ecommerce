from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.users.daos.user import user_dao
from app.exceptions.custom import IncorrectCredentials

from app.core import deps
from app.auth.serializers.token import TokenGrantType, TokenReadSerializer
from app.auth.serializers.auth import LoginSerializer

router = APIRouter()


@router.post("/access-token", response_model=TokenReadSerializer)
async def login_for_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = user_dao.authenticate_user(
        db, username=form_data.username, password=form_data.password
    )

    if not user:
        raise IncorrectCredentials

    return create_access_token(
        data={
            "sub": user.phone, 
            "scopes": form_data.scopes,
            "grant_type": TokenGrantType.CLIENT_CREDENTIALS.value
        },
    )

@router.post("/login", response_model=TokenReadSerializer)
async def login(
    login_data: LoginSerializer,
    db: Session = Depends(deps.get_db),
) -> TokenReadSerializer:
    pass


# On login
# Create new access token
# Save it to db
# Return saved access token

# On login
# Fetch user_id
# Get access token from db
# If valid contiue