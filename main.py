from datetime import datetime, timedelta
from typing import List, Union

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from app.core.config import get_app_settings
from datetime import datetime
from app.users.serializers.user import UserBaseSerializer, UserCreateSerializer
#serializers.user import UserBaseSerializer, UserCreateSerializer
from app.core.deps import get_async_db, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
import fastapi

settings = get_app_settings()

fake_users_db = {
    "254704845045": {
        "id": "a",
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "phone": "254704845045",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_active": True,
        "user_type": "ADMIN",
        "date_joined": datetime.strptime('26 Sep 2012', '%d %b %Y')
    },
    "254704845043": {
        "id": "b",
        "first_name": "Alice",
        "last_name": "Homes",
        "email": "alice@example.com",
        "phone": "254704845043",
        "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_active": False,
        "user_type": "CUSTOMER",
        "date_joined": datetime.strptime('26 Sep 2012', '%d %b %Y')
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    phone: Union[str, None] = None
    scopes: List[str] = []


class User(BaseModel):
    phone: str
    email: Union[str, None] = None
    first_name: Union[str, None] = None
    is_active: Union[bool, None] = None


class UserInDB(User):
    password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

app = FastAPI()
from app.users.routes import user
router = fastapi.APIRouter()
router.include_router(user.router, prefix="/users")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, phone: str):
    if phone in db:
        user_dict = db[phone]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, phone: str, password: str):
    user = get_user(fake_db, phone)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, phone=phone)

    except (JWTError, ValidationError):
        raise credentials_exception

    user = get_user(fake_users_db, phone=token_data.phone)

    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user


async def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=["me"])
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect phone or password")

    access_token_expires = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRY_IN_SECONDS)
    access_token = create_access_token(
        data={"sub": user.phone, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: User = Security(get_current_active_user, scopes=["items"])
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/status/")
async def read_system_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    from app.users.daos.user import user_dao
    return user_dao.get_all(db)
    # return {"status": "ok"}


@app.patch("/users/update", response_model=UserBaseSerializer)
def update_user(
    user: UserCreateSerializer,
    _: User = Security(get_current_active_user, scopes=["items"])
):
    return user
