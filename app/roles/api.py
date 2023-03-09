from fastapi import APIRouter
from app.roles.routes import user_role
from app.roles.routes import role


router = APIRouter(prefix="/roles", tags=["roles"])
router.include_router(role.router)
router.include_router(user_role.router)
