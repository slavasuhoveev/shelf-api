"""Pydantic schemas for shelf and storage endpoints."""

from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from pydantic import Field, constr

from shelf.app.enums.shelf import (
    StorageType,
)

from shelf.app.schemas.base import BaseShelfModel as BaseModel


# StorageSlot model

class StorageSlotCreate(BaseModel):
    """Pydatic schema for StorageSlot object creation."""

    storage_item_id: UUID
    user_album_id: Optional[UUID] = None
    position: dict
    capacity: Annotated[int, Field(ge=1)] = 1


class StorageSlotRead(BaseModel):
    """Pydatic schema for StorageSlot object getting."""

    id: UUID
    storage_item_id: UUID
    user_album_id: Optional[UUID] = None
    position: dict
    capacity: int
    created_at: datetime
    updated_at: datetime


class StorageSlotUpdate(BaseModel):
    """Pydatic schema for StorageSlot object updating."""

    storage_item_id: Optional[UUID] = None
    user_album_id: Optional[UUID] = None
    position: Optional[dict] = None
    capacity: Optional[Annotated[int, Field(ge=1)]] = None


# StorageItem model

class StorageItemCreate(BaseModel):
    """Pydatic schema for StorageItem object creation."""

    group_id: Optional[UUID] = None
    title: Optional[Annotated[str, constr(min_length=1, max_length=100)]] = None
    description: Optional[Annotated[str, constr(min_length=1, max_length=250)]] = None
    is_public: bool = False
    storage_type: StorageType
    form_vector: dict
    position_vector: Optional[dict]
    storage_slots: Optional[list[StorageSlotCreate]] = None


class StorageItemRead(BaseModel):
    """Pydatic schema for StorageItem object getting."""

    id: UUID
    user_id: UUID
    group_id: Optional[UUID] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_public: bool
    storage_type: StorageType
    form_vector: dict
    position_vector: Optional[dict] = None
    storage_slots: Optional[list[StorageSlotRead]] = None
    created_at: datetime
    updated_at: datetime


class StorageItemUpdate(BaseModel):
    """Pydatic schema for StorageItem object updating."""

    group_id: Optional[UUID] = None
    title: Optional[Annotated[str, constr(min_length=1, max_length=100)]] = None
    description: Optional[Annotated[str, constr(min_length=1, max_length=250)]] = None
    is_public: Optional[bool] = None
    storage_type: Optional[StorageType] = None
    form_vector: Optional[dict] = None
    position_vector: Optional[dict] = None


# StorageGroup model

class StorageGroupCreate(BaseModel):
    """Pydatic schema for StorageGroup object creation."""

    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=250)
    is_public: bool = False


class StorageGroupRead(BaseModel):
    """Pydatic schema for StorageGroup object getting."""

    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    is_public: bool
    storage_items: Optional[list[StorageItemRead]] = None
    created_at: datetime
    updated_at: datetime


class StorageGroupUpdate(BaseModel):
    """Pydatic schema for StorageGroup object updating."""

    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1, max_length=250)
    is_public: Optional[bool] = None
