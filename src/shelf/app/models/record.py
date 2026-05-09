"""ORM models for record-related entities.

Defines AlbumWork, Release, and related database structures.
"""

import uuid
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, ARRAY, Enum as SQLEnum, JSON
from sqlalchemy.dialects.postgresql import UUID

from shelf.app.enums.record import (
    MediumFormat,
    RecordGrade,
    SleeveGrade,
)

from shelf.app.models.shelf import StorageSlot

from shelf.app.models.base import BaseModel


class AlbumWork(BaseModel):
    """Represents an album as an artistic work.

    Fields:
        id: Unique album identifier (UUID).
        title: Title of the album.
        artist: Name of the artist or band.
        year_composed: Year the album was composed.
        genre: Album genre.
        style: Music style.
        tracks: List of track titles on the album.
        notes: Additional notes about the album.
        created_by: User ID who created this entry.
        updated_by: User ID who updated this entry.
        is_verified: Whether the album entry is verified.
        is_public: Whether the album entry is publicly visible.
    """

    __tablename__ = 'album_works'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    artist: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    year_composed: Mapped[int] = mapped_column(index=True, nullable=False)
    genre: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    style: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    tracks: Mapped[list[str]] = mapped_column(ARRAY(String(100)), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=True)
    is_verified: Mapped[bool] = mapped_column(server_default='false', index=True, nullable=False)
    is_public: Mapped[bool] = mapped_column(server_default='false', index=True, nullable=False)

    releases: Mapped[list['Release']] = relationship(
        back_populates='album_work', cascade='all, delete-orphan', lazy='selectin'
    )

    def __repr__(self) -> str:
        """AlbumWork representation string."""
        return f'Album work: {self.title}'


class Release(BaseModel):
    """Represents an album as a release.

    Fields:
        id: Unique album identifier (UUID).
        album_work_id: related album work identifier (UUID).
        label: Label that released the album.
        country: Country in which album was released.
        year: Year the album was released.
        tracks: List of track titles on the released album.
        notes: Additional notes about the album.
        created_by: User ID who created this entry.
        updated_by: User ID who updated this entry.
        is_verified: Whether the album entry is verified.
        is_public: Whether the album entry is publicly visible.
    """

    __tablename__ = 'releases'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    album_work_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('album_works.id'), nullable=False)
    label: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    year: Mapped[int] = mapped_column(index=True, nullable=False)
    tracklist: Mapped[list[str]] = mapped_column(
        # Postgres array
        ARRAY(String(100)),
        nullable=False,
    )
    notes: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=True)
    is_verified: Mapped[bool] = mapped_column(server_default='false', index=True, nullable=False)
    is_public: Mapped[bool] = mapped_column(server_default='true', index=True, nullable=False)

    album_work = relationship('AlbumWork', back_populates='releases', lazy='selectin')

    mediums: Mapped[list['Medium']] = relationship(
        back_populates='release', cascade='all, delete-orphan', lazy='selectin'
    )

    def __repr__(self) -> str:
        """Release representation string."""
        return f'Release {self.id} of album {self.album_work_id}'


class Medium(BaseModel):
    """Represents an album as a specific album medium: LP, CD, Cassette etc.

    Fields:
        id: Unique album identifier (UUID).
        release_id: related album release identifier (UUID).
        format: Medium format (LP, CD, Cassette).
        medium_count: Number of mediums for single album.
        sides: Dict of track titles on the medium.
        color_hint: Album main collor hint.
        notes: Additional notes about the album.
        created_by: User ID who created this entry.
        updated_by: User ID who updated this entry.
        is_verified: Whether the album entry is verified.
        is_public: Whether the album entry is publicly visible.
    """

    __tablename__ = 'mediums'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    release_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('releases.id'), nullable=False)
    format: Mapped[MediumFormat] = mapped_column(
        SQLEnum(MediumFormat, name='medium_format'), index=True, nullable=False
    )
    medium_count: Mapped[int] = mapped_column(nullable=False)
    sides: Mapped[list[dict]] = mapped_column(JSON, nullable=False)
    color_hint: Mapped[str] = mapped_column(String(10), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=False)
    updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, nullable=True)
    is_verified: Mapped[bool] = mapped_column(server_default='false', index=True, nullable=False)
    is_public: Mapped[bool] = mapped_column(server_default='true', index=True, nullable=False)

    release = relationship('Release', back_populates='mediums', lazy='selectin')

    user_albums: Mapped[list['UserAlbum']] = relationship(
        back_populates='medium', cascade='all, delete-orphan', lazy='selectin'
    )

    def __repr__(self) -> str:
        """Medium representation string."""
        return f'Medium {self.id} of release {self.release_id}'


class UserAlbum(BaseModel):
    """Represents an album as a specific user item.

    Fields:
        id: Unique album identifier (UUID).
        user_id: Unique user identifier (UUID).
        medium_id: related album medium identifier (UUID).
        storage_slot: related album position in shelf identifier (UUID).
        custom_notes: Additional user notes about the album.
        custom_cover: Cover url (str).
        vinyl_grade: Vinyl shape grade.
        sleeve_grade: Sleeve shape grade.
        is_shared: Is user shared his album to others.
    """

    __tablename__ = 'user_albums'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    medium_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('mediums.id'), nullable=False)
    custom_notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    custom_cover: Mapped[Optional[str]] = mapped_column(nullable=True)
    vinyl_grade: Mapped[Optional[RecordGrade]] = mapped_column(SQLEnum(RecordGrade, name='vinyl_grade'), nullable=True)
    sleeve_grade: Mapped[Optional[SleeveGrade]] = mapped_column(
        SQLEnum(SleeveGrade, name='sleeve_grade'), nullable=True
    )
    is_shared: Mapped[bool] = mapped_column(server_default='false', nullable=False)

    medium = relationship('Medium', back_populates='user_albums', lazy='selectin')

    storage_slot: Mapped[Optional[StorageSlot]] = relationship(
        StorageSlot,
        back_populates='user_album',
        uselist=False,
    )

    def __repr__(self) -> str:
        """UserAlbum representation string."""
        return f'User album {self.id} of medium {self.medium_id}'
