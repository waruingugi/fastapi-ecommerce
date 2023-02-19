from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.users.daos.user import user_dao
from app.exceptions.custom import IncorrectCredentials

from app.core import deps
from app.auth.serializers.token import (
    TokenReadSerializer
)
from app.auth.serializers.auth import LoginSerializer
from app.auth.utils.login import login_user

router = APIRouter()


@router.post("/access-token", response_model=TokenReadSerializer)
async def login_for_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Get access token for future requests"""
    login_data = LoginSerializer(username=form_data.username, password=form_data.password)
    token = login_user(db, login_data=login_data)
    return token


@router.post("/login", response_model=TokenReadSerializer)
async def login(
    login_data: LoginSerializer,
    db: Session = Depends(deps.get_db),
) -> TokenReadSerializer:
    token = login_user(db, login_data=login_data)
    return token


# On login
# Create new access token
# Save it to db
# Return saved access token

# On login
# Fetch user_id
# Get access token from db
# If valid contiue
# If invalid, check refresh token is valid
# Issue new access token n refresh token
# Invalidate previous tokens linked with user
# If is invalid, 
# Ask user to log in again
# If user uses invalid token raise waring of hacker