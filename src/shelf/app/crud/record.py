"""CRUD operations for record-related models.

Includes creation, update, deletion, and retrieval
logic for album works and releases.
"""

from sqlalchemy.orm import Session
from shelf.app.models.record import (
    AlbumWork,
    Release,
    Medium,
    UserAlbum,
)
from shelf.app.schemas.record import (
    AlbumWorkCreate,
    AlbumWorkUpdate,
    ReleaseCreate,
    ReleaseUpdate,
    MediumCreate,
    MediumUpdate,
    UserAlbumCreate,
    UserAlbumUpdate,
)
from uuid import UUID


# AlbumWork model crud


def create_album_work(
    db: Session,
    album_in: AlbumWorkCreate,
    user_id: UUID,
) -> AlbumWork:
    """Create a new AlbumWork record in the database.

    Args:
    ----
        db (Session): SQLAlchemy session.
        album_in (AlbumWorkCreate): Pydantic input with fields to create.
        user_id (UUID): user ID performing the album work creation.

    Returns:
    -------
        AlbumWork: the created AlbumWork ORM object.

    """
    obj = AlbumWork(
        title=album_in.title,
        artist=album_in.artist,
        year_composed=album_in.year_composed,
        genre=album_in.genre,
        style=album_in.style,
        tracks=album_in.tracks,
        notes=album_in.notes,
        is_public=album_in.is_public,
        created_by=user_id,
        updated_by=user_id,
        is_verified=False,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_album_work(db: Session, album_id: UUID) -> AlbumWork | None:
    """Retrieve a single AlbumWork by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        album_id (UUID): album work ID.

    Returns:
    -------
        AlbumWork | None: the found AlbumWork object or None.

    """
    return db.query(AlbumWork).filter(AlbumWork.id == album_id).first()


def get_album_works(db: Session, skip: int = 0, limit: int = 100) -> list[AlbumWork]:
    """Retrieve a list of AlbumWork records with pagination.

    Args:
    ----
        db (Session): SQLAlchemy session.
        skip (int): number of records to skip.
        limit (int): max number of records to return.

    Returns:
    -------
        list[AlbumWork]: list of AlbumWork ORM objects.

    """
    return db.query(AlbumWork).offset(skip).limit(limit).all()


def update_album_work(
    db: Session,
    db_obj: AlbumWork,
    album_in: AlbumWorkUpdate,
    user_id: UUID,
) -> AlbumWork:
    """Update an existing AlbumWork record partially.

    Args:
    ----
        db (Session): SQLAlchemy session.
        db_obj (AlbumWork): existing ORM object.
        album_in (AlbumWorkUpdate): Pydantic input with fields to update.
        user_id (UUID): user ID performing the update.

    Returns:
    -------
        AlbumWork: updated AlbumWork ORM object.

    """
    data = album_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)

    db_obj.is_verified = False  # reset verification on any change
    db_obj.updated_by = user_id

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_album_work(db: Session, album_id: UUID) -> None:
    """Delete an AlbumWork record by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        album_id (UUID): album work ID to delete.

    Returns:
    -------
        None

    """
    obj = db.query(AlbumWork).filter(AlbumWork.id == album_id).first()
    if obj:
        db.delete(obj)
        db.commit()


# Release model crud


def create_release(
    db: Session,
    release_in: ReleaseCreate,
    user_id: UUID,
) -> Release:
    """Create a new Release record in the database.

    Args:
    ----
        db (Session): SQLAlchemy session.
        release_in (ReleaseCreate): Pydantic input with fields to create.
        user_id (UUID): user ID performing the release creation.

    Returns:
    -------
        Release: the created Release ORM object.

    """
    obj = Release(
        album_work_id=release_in.album_work_id,
        label=release_in.label,
        country=release_in.country,
        year=release_in.year,
        tracklist=release_in.tracklist,
        notes=release_in.notes,
        created_by=user_id,
        updated_by=user_id,
        is_verified=False,
        is_public=release_in.is_public,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_release(db: Session, release_id: UUID) -> Release | None:
    """Retrieve a single Release by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        release_id (UUID): release ID.

    Returns:
    -------
        Release | None: the found Release object or None.

    """
    return db.query(Release).filter(Release.id == release_id).first()


def get_releases(db: Session, skip: int = 0, limit: int = 100) -> list[Release]:
    """Retrieve a list of Release records with pagination.

    Args:
    ----
        db (Session): SQLAlchemy session.
        skip (int): number of records to skip.
        limit (int): max number of records to return.

    Returns:
    -------
        list[Release]: list of Release ORM objects.

    """
    return db.query(Release).offset(skip).limit(limit).all()


def update_release(
    db: Session,
    db_obj: Release,
    release_in: ReleaseUpdate,
    user_id: UUID,
) -> Release:
    """Update an existing Release record partially.

    Args:
    ----
        db (Session): SQLAlchemy session.
        db_obj (Release): existing ORM object.
        release_in (ReleaseUpdate): Pydantic input with fields to update.
        user_id (UUID): user ID performing the update.

    Returns:
    -------
        Release: updated Release ORM object.

    """
    data = release_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)

    db_obj.is_verified = False  # reset verification on any change
    db_obj.updated_by = user_id

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_release(db: Session, release_id: UUID) -> None:
    """Delete a Release record by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        release_id (UUID): release ID to delete.

    Returns:
    -------
        None

    """
    obj = db.query(Release).filter(Release.id == release_id).first()
    if obj:
        db.delete(obj)
        db.commit()


# Medium model crud


def create_medium(
    db: Session,
    medium_in: MediumCreate,
    user_id: UUID,
) -> Medium:
    """Create a new Medium record in the database.

    Args:
    ----
        db (Session): SQLAlchemy session.
        medium_in (MediumCreate): Pydantic input with fields to create.
        user_id (UUID): user ID performing the medium creation.

    Returns:
    -------
        Medium: the created Medium ORM object.

    """
    obj = Medium(
        release_id=medium_in.release_id,
        format=medium_in.format,
        medium_count=medium_in.medium_count,
        sides=medium_in.sides,
        color_hint=medium_in.color_hint,
        notes=medium_in.notes,
        created_by=user_id,
        updated_by=user_id,
        is_verified=False,
        is_public=medium_in.is_public,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_medium(db: Session, medium_id: UUID) -> Medium | None:
    """Retrieve a single Medium by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        medium_id (UUID): medium ID.

    Returns:
    -------
        Medium | None: the found Medium object or None.

    """
    return db.query(Medium).filter(Medium.id == medium_id).first()


def get_mediums(db: Session, skip: int = 0, limit: int = 100) -> list[Medium]:
    """Retrieve a list of Medium records with pagination.

    Args:
    ----
        db (Session): SQLAlchemy session.
        skip (int): number of records to skip.
        limit (int): max number of records to return.

    Returns:
    -------
        list[Medium]: list of Medium ORM objects.

    """
    return db.query(Medium).offset(skip).limit(limit).all()


def update_medium(
    db: Session,
    db_obj: Medium,
    medium_in: MediumUpdate,
    user_id: UUID,
) -> Medium:
    """Update an existing Medium record partially.

    Args:
    ----
        db (Session): SQLAlchemy session.
        db_obj (Medium): existing ORM object.
        medium_in (MediumUpdate): Pydantic input with fields to update.
        user_id (UUID): user ID performing the update.

    Returns:
    -------
        Medium: updated Medium ORM object.

    """
    data = medium_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)

    db_obj.is_verified = False  # reset verification on any change
    db_obj.updated_by = user_id

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_medium(db: Session, medium_id: UUID) -> None:
    """Delete a Medium record by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        medium_id (UUID): medium ID to delete.

    Returns:
    -------
        None

    """
    obj = db.query(Medium).filter(Medium.id == medium_id).first()
    if obj:
        db.delete(obj)
        db.commit()


# UserAlbum model crud


def create_user_album(
    db: Session,
    user_album_in: UserAlbumCreate,
    user_id: UUID,
) -> UserAlbum:
    """Create a new UserAlbum record in the database.

    Args:
    ----
        db (Session): SQLAlchemy session.
        user_album_in (UserAlbumCreate): Pydantic input with fields to create.
        user_id (UUID): user ID performing the user album creation.

    Returns:
    -------
        UserAlbum: the created UserAlbum ORM object.

    """
    obj = UserAlbum(
        user_id=user_id,
        medium_id=user_album_in.medium_id,
        custom_notes=user_album_in.custom_notes,
        custom_cover=user_album_in.custom_cover,
        vinyl_grade=user_album_in.vinyl_grade,
        sleeve_grade=user_album_in.sleeve_grade,
        is_shared=user_album_in.is_shared,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_user_album(db: Session, user_album_id: UUID) -> UserAlbum | None:
    """Retrieve a single UserAlbum by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        user_album_id (UUID): user album ID.

    Returns:
    -------
        UserAlbum | None: the found UserAlbum object or None.

    """
    return db.query(UserAlbum).filter(UserAlbum.id == user_album_id).first()


def get_user_albums(db: Session, skip: int = 0, limit: int = 100) -> list[UserAlbum]:
    """Retrieve a list of UserAlbum records with pagination.

    Args:
    ----
        db (Session): SQLAlchemy session.
        skip (int): number of records to skip.
        limit (int): max number of records to return.

    Returns:
    -------
        list[UserAlbum]: list of UserAlbum ORM objects.

    """
    return db.query(UserAlbum).offset(skip).limit(limit).all()


def update_user_album(
    db: Session,
    db_obj: UserAlbum,
    user_album_in: UserAlbumUpdate,
) -> UserAlbum:
    """Update an existing UserAlbum record partially.

    Args:
    ----
        db (Session): SQLAlchemy session.
        db_obj (UserAlbum): existing ORM object.
        user_album_in (UserAlbumUpdate): Pydantic input with fields to update.

    Returns:
    -------
        UserAlbum: updated UserAlbum ORM object.

    """
    data = user_album_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_user_album(db: Session, user_album_id: UUID) -> None:
    """Delete a UserAlbum record by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        user_album_id (UUID): user album ID to delete.

    Returns:
    -------
        None

    """
    obj = db.query(UserAlbum).filter(UserAlbum.id == user_album_id).first()
    if obj:
        db.delete(obj)
        db.commit()
