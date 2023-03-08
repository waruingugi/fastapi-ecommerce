# Import all the models, so that Base has them before being
# imported by Alembic
from app.business_partner.models import *  # noqa
from app.users.models import *  # noqa
from app.auth.models import *  # noqa
from app.roles.models import *  # noqa
from app.common.models import *  # noqa
from app.db.base_class import Base  # noqa
