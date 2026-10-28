import os
from collections.abc import Iterator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

def _get_database_url() -> str:
    env_path: Path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)

    database_url: str | None = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("Set DATABASE_URL in .env or the process environment")

    return database_url


_engine: Engine = create_engine(_get_database_url(), pool_pre_ping=True)
_sessionmaker: sessionmaker[Session] = sessionmaker(
    bind=_engine,
    expire_on_commit=False,
)


def get_session() -> Iterator[Session]:
    with _sessionmaker() as session:
        yield session
