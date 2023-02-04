from fastapi import APIRouter
from app.users.routes import user

router = APIRouter(prefix="/users", tags=["users"])

router.include_router(user.router)
