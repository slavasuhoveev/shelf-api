"""Base SQLAlchemy model definitions.

Contains shared fields and declarative base configuration.
"""

from datetime import datetime

from sqlalchemy import func

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """Base Shelf model class."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )
