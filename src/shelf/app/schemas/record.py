"""Pydantic schemas for record-related endpoints."""

from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from pydantic import (
    Field, constr,
)

from shelf.app.enums.record import (
    MediumFormat,
    RecordGrade,
    SleeveGrade,
)

from shelf.app.schemas.base import BaseShelfModel as BaseModel


# AlbumWork model

class AlbumWorkCreate(BaseModel):
    """Pydatic schema for AlbumWork object creation."""

    title: Annotated[str, constr(min_length=1, max_length=255)]
    artist: Annotated[str, constr(min_length=1, max_length=255)]
    year_composed: Annotated[int, Field(ge=1900, le=2100)]
    genre: Annotated[str, constr(min_length=1, max_length=50)]
    style: Annotated[str, constr(min_length=1, max_length=100)]
    tracks: list[Annotated[str, constr(min_length=1)]]
    notes: Optional[str] = None
    is_public: bool = False


class AlbumWorkRead(BaseModel):
    """Pydatic schema for AlbumWork object reading."""

    id: UUID
    title: str
    artist: str
    year_composed: int
    genre: str
    style: str
    tracks: list[str]
    notes: Optional[str] = None
    created_by: UUID
    updated_by: Optional[UUID] = None
    is_verified: bool
    is_public: bool
    created_at: datetime
    updated_at: datetime


class AlbumWorkUpdate(BaseModel):
    """Pydatic schema for AlbumWork object updating."""

    title: Optional[Annotated[str, constr(min_length=1, max_length=255)]] = None
    artist: Optional[Annotated[str, constr(min_length=1, max_length=255)]] = None
    year_composed: Optional[int] = Field(None, ge=1900, le=2100)
    genre: Optional[Annotated[str, constr(min_length=1, max_length=50)]] = None
    style: Optional[Annotated[str, constr(min_length=1, max_length=100)]] = None
    tracks: Optional[list[Annotated[str, constr(min_length=1)]]] = None
    notes: Optional[str] = None
    is_public: Optional[bool] = None


# Release model

class ReleaseCreate(BaseModel):
    """Pydatic schema for Release object creation."""

    album_work_id: UUID
    label: Optional[Annotated[str, constr(min_length=1, max_length=100)]]
    country: Optional[Annotated[str, constr(min_length=1, max_length=100)]]
    year: Annotated[int, Field(ge=1900, le=2100)]
    tracklist: list[Annotated[str, constr(min_length=1)]]
    notes: Optional[str]
    is_verified: bool = False
    is_public: bool = False


class ReleaseRead(BaseModel):
    """Pydatic schema for Release object getting."""

    id: UUID
    album_work_id: UUID
    label: Optional[str] = None
    country: Optional[str] = None
    year: int
    tracklist: list[str]
    notes: Optional[str] = None
    created_by: UUID
    updated_by: Optional[UUID] = None
    is_verified: bool
    is_public: bool
    created_at: datetime
    updated_at: datetime


class ReleaseUpdate(BaseModel):
    """Pydatic schema for Release object updating."""

    album_work_id: Optional[UUID] = None
    label: Optional[Annotated[str, constr(min_length=1, max_length=100)]] = None
    country: Optional[Annotated[str, constr(min_length=1, max_length=100)]] = None
    year: Optional[Annotated[int, Field(ge=1900, le=2100)]] = None
    tracklist: Optional[list[Annotated[str, constr(min_length=1)]]] = None
    notes: Optional[str] = None
    is_verified: Optional[bool] = None
    is_public: Optional[bool] = None


# Medium model

class MediumCreate(BaseModel):
    """Pydatic schema for Medium object creation."""

    release_id: UUID
    format: MediumFormat
    medium_count: Annotated[int, Field(ge=1)]
    sides: list[dict]
    color_hint: Annotated[str, constr(min_length=1, max_length=10)]
    notes: Optional[str] = None
    is_public: bool = False


class MediumRead(BaseModel):
    """Pydatic schema for Medium object getting."""

    id: UUID
    release_id: UUID
    format: MediumFormat
    medium_count: int
    sides: list[dict]
    color_hint: str
    notes: Optional[str] = None
    created_by: UUID
    updated_by: Optional[UUID] = None
    is_verified: bool
    is_public: bool
    created_at: datetime
    updated_at: datetime


class MediumUpdate(BaseModel):
    """Pydatic schema for Medium object updating."""

    release_id: Optional[UUID] = None
    format: Optional[MediumFormat] = None
    medium_count: Optional[Annotated[int, Field(ge=1)]] = None
    sides: Optional[list[dict]] = None
    color_hint: Optional[Annotated[str, constr(min_length=1, max_length=10)]] = None
    notes: Optional[str] = None
    is_public: Optional[bool] = None


# UserAlbum model

class UserAlbumCreate(BaseModel):
    """Pydatic schema for UserAlbumm object creation."""

    medium_id: UUID
    slot_id: Optional[UUID] = None
    custom_notes: Optional[Annotated[str, constr(min_length=1, max_length=500)]] = None
    custom_cover: Optional[str] = None
    vinyl_grade: Optional[RecordGrade] = None
    sleeve_grade: Optional[SleeveGrade] = None
    is_shared: bool = False


class UserAlbumRead(BaseModel):
    """Pydatic schema for UserAlbumm object getting."""

    id: UUID
    user_id: UUID
    medium_id: UUID
    slot_id: Optional[UUID] = None
    custom_notes: Optional[str] = None
    custom_cover: Optional[str] = None
    vinyl_grade: Optional[RecordGrade] = None
    sleeve_grade: Optional[SleeveGrade] = None
    is_shared: bool
    created_at: datetime
    updated_at: datetime


class UserAlbumUpdate(BaseModel):
    """Pydatic schema for UserAlbumm object updating."""

    medium_id: Optional[UUID] = None
    slot_id: Optional[UUID] = None
    custom_notes: Optional[Annotated[str, constr(min_length=1, max_length=500)]] = None
    custom_cover: Optional[str] = None
    vinyl_grade: Optional[RecordGrade] = None
    sleeve_grade: Optional[SleeveGrade] = None
    is_shared: Optional[bool] = None
