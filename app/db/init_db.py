import logging
from sqlalchemy.orm import Session

from app.users.daos.user import user_dao
from app.users.serializers.user import UserCreateSerializer
from app.users.constants import UserTypes
from app.db import base  # noqa

from app.core.config import get_app_settings



logger = logging.getLogger(__name__)


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables by un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    settings = get_app_settings()

    if settings.SUPERUSER_EMAIL:
        user = user_dao.get_by_email(db, email=settings.SUPERUSER_EMAIL)

        if not user:
            user_in = UserCreateSerializer(
                first_name=settings.SUPERUSER_FIRST_NAME,
                last_name=settings.SUPERUSER_LAST_NAME,
                phone=settings.SUPERUSER_PHONE,
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD,
                user_type=UserTypes.SUPERADMIN.value,
                is_active=True
            )
            user = user_dao.create(db, obj_in=user_in)  # noqa
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.SUPERUSER_EMAIL} already exists. "
            )
