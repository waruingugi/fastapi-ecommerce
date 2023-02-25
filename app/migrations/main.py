from fastapi import Depends
from sqlalchemy.orm import Session
from app.core import deps
import os
import importlib
import sys


ROOT_DIR = os.path.abspath(os.curdir)
MIGRATION_SCRIPTS_PATH = f"{ROOT_DIR}/app/migrations/scripts/"


def get_module_name(revision: str) -> str | None:
    """Get module name if file exists"""
    file_path = f"{MIGRATION_SCRIPTS_PATH}/{revision}.py"
    file_path_exists = os.path.isfile(file_path)

    if file_path_exists:
        dirname, basename = os.path.split(file_path)

        if dirname not in sys.path:
            sys.path.append(dirname)

        return os.path.splitext(basename)[0]

    return None



def run_migration_scripts(
    *,
    revision: str,
    migration_type: str,
    db: Session = Depends(deps.get_db),
) -> None:
    """Run migration script related to specific alembic version"""
    module_name = get_module_name(revision)

    if module_name:
        module = importlib.import_module(module_name)

        # Run migration scripts
        if migration_type == 'pre':
            module.pre_migrate()
        
        if migration_type == 'post':
            module.post_migrate()
