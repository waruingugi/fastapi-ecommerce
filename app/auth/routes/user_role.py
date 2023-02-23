# Route
# User role serializer
# Is superadmin

from app.core import deps
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/")
async def create_user_role(
    db: Session = Depends(deps.get_db),
):
    pass
