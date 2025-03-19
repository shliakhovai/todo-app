import logging
from os import getenv
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT", "5432")
DB_NAME = getenv("DB_NAME")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")

if not all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
    raise ValueError("Missing environment variables for database connection.")

DATABASE_URL = URL.create(
    drivername="postgresql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for transactional operations."""
    db = SessionLocal()
    try:
        yield db
    except Exception as error:
        db.rollback()
        _logger.error(f"Database transaction error: {error}")
        raise
    finally:
        db.close()


_logger = logging.getLogger(__name__)
