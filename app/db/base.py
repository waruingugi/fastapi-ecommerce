# Import all the models, so that Base has them before being
# imported by Alembic
from app.business.models import *  # noqa
from app.users.models import *
from app.db.base_class import Base
