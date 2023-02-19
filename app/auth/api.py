from fastapi import APIRouter
from app.auth.routes import login
from app.auth.routes import token


router = APIRouter(prefix="/auth", tags=["login"])
router.include_router(login.router)
router.include_router(token.router)
