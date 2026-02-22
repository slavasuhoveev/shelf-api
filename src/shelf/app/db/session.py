"""Database session management.

Provides SQLAlchemy session factory and dependency
for FastAPI route handlers.
"""

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from shelf.app.core.config import settings


engine = create_engine(
    settings.postgres_url,
    poolclass=NullPool,
    future=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
