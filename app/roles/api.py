from fastapi import APIRouter
from app.roles.routes import user_role


router = APIRouter(prefix="/roles", tags=["roles"])
router.include_router(user_role.router)
