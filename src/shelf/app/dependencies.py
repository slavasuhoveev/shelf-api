from sqlalchemy.orm import Session
from typing import Generator

from shelf.app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy database session and ensure it is properly closed.

    Args:
    ----
        None

    Returns:
    -------
    Generator[Session, None, None]: a generator yielding a database session.

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_id():
    ...
