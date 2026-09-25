import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# 1. Add the root project directory to Python's path so it can find the 'app' module
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 2. Load the .env file
load_dotenv()

# 3. Import your SQLAlchemy Base
from app.models import Base

config = context.config

# 4. Override the sqlalchemy.url in alembic.ini with the one from your .env
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 5. Point Alembic to your model metadata
target_metadata = Base.metadata