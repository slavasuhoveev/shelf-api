"""ORM models for shelf and storage entities."""

import uuid
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    String,
    Enum as SQLEnum,
    JSON,
)
from sqlalchemy.dialects.postgresql import UUID

from shelf.app.models.base import BaseModel
from shelf.app.enums.shelf import StorageType


class StorageSlot(BaseModel):
    """Represents a user-defined storage slot for user album.

    Fields:
        id: Unique group identifier (UUID).
        storage_item_id: related storage item identifier (UUID).
        user_album_id: related user album item identifier (UUID).
        position: JSON vector position.
        capacity: Storage slot capacity.
    """

    __tablename__ = 'storage_slots'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    storage_item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('storage_items.id'), nullable=False)
    user_album_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user_albums.id'), nullable=True, unique=True)
    position: Mapped[dict] = mapped_column(JSON, nullable=False)
    capacity: Mapped[int] = mapped_column(server_default='1', nullable=False)

    storage_item = relationship('StorageItem', back_populates='storage_slots', lazy='selectin')
    user_album = relationship(
        'UserAlbum',
        back_populates='storage_slot',
        lazy='selectin',
        uselist=False,
        foreign_keys=[user_album_id],
    )

    def __repr__(self) -> str:
        """StorageSlot representation string."""
        return f'Storage slot {self.id} of medium {self.user_album_id}'


class StorageItem(BaseModel):
    """Represents a user-defined storage item (shelf, frame).

    Fields:
        id: Unique group identifier (UUID).
        user_id: Unique user identifier (UUID).
        group_id: related storage group identifier (UUID).
        title: Item title.
        description: Item description.
        storage_type: Storage item type (shelf, frame).
        form_vector: JSON item form coordinats
        position_vector: JSON item position coordinats
        is_public: Whether this group is publicly visible to others.
    """

    __tablename__ = 'storage_items'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    group_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey('storage_groups.id'), nullable=True)
    title: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    is_public: Mapped[bool] = mapped_column(server_default='false', nullable=False)
    storage_type: Mapped[StorageType] = mapped_column(SQLEnum(StorageType, name='storage_type'), nullable=False)
    form_vector: Mapped[dict] = mapped_column(JSON, nullable=False)
    position_vector: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    storage_group: Mapped[Optional['StorageGroup']] = relationship(
        'StorageGroup', back_populates='storage_items', lazy='selectin'
    )

    storage_slots: Mapped[list['StorageSlot']] = relationship(
        back_populates='storage_item', cascade='all, delete-orphan', lazy='selectin'
    )

    def __repr__(self) -> str:
        """StorageItem representation string."""
        return f'{self.storage_type} storage {self.title if self.title else self.id}'


class StorageGroup(BaseModel):
    """Represents a user-defined storage group to organize albums.

    Fields:
        id: Unique group identifier (UUID).
        user_id: Unique user identifier (UUID).
        title: Title of the group.
        description: Description of the group.
        is_public: Whether this group is publicly visible to others.
        storage_items: List of storage items in this group.
    """

    __tablename__ = 'storage_groups'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    is_public: Mapped[bool] = mapped_column(server_default='false', nullable=False)

    storage_items: Mapped[list['StorageItem']] = relationship(
        back_populates='storage_group', cascade='all, delete-orphan', lazy='selectin'
    )

    def __repr__(self) -> str:
        """StorageGroup representation string."""
        return f'Storage group {self.title}'
