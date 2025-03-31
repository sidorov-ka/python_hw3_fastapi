import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# Пути
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Логгирование
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Импорт моделей
from src.models import Base
target_metadata = Base.metadata

# Получаем URL без set_section_option
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL is not set")

def run_migrations_offline():
    """Run migrations in offline mode."""
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in online mode."""
    from sqlalchemy import create_engine
    connectable = create_engine(database_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
