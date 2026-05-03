from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app.db.session import Base
import app.db.models as models

from alembic import context

config = context.config

# Alembic uses the sync psycopg2 driver — strip +asyncpg and fix ssl param
_db_url = (
    os.getenv("DATABASE_URL", "")
    .replace("+asyncpg", "")
    .replace("ssl=require", "sslmode=require")
)
config.set_main_option("sqlalchemy.url", _db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

IGNORED_TABLES = {"langchain_pg_collection", "langchain_pg_embedding"}

def include_object(_object, name, type_, _reflected, _compare_to):
    if type_ == "table" and name in IGNORED_TABLES:
        return False
    return True


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
