#! /bin/sh

# Uncomment command below if you are having 
# ´ModuleNotFoundError: No module named 'app´ errors 
export PYTHONPATH=$PWD

# Let the DB start
python app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python app/initial_data.py