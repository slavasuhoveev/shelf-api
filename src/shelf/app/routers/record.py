"""API routes for record-related endpoints."""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response,
)
from sqlalchemy.orm import Session
from uuid import UUID

from shelf.app.schemas import record as record_schemas
from shelf.app.crud import record as record_crud
from shelf.app.schemas.auth import TokenPayload
from shelf.app.dependencies import get_db, require_auth, get_token_payload
from shelf.app.models import record as record_models

album_work_router = APIRouter(
    prefix='/api/album-works',
    dependencies=[Depends(require_auth)],
    tags=['Record', 'Album Work'],
)
release_router = APIRouter(
    prefix='/api/releases',
    dependencies=[Depends(require_auth)],
    tags=['Record', 'Release'],
)
medium_router = APIRouter(
    prefix='/api/mediums',
    dependencies=[Depends(require_auth)],
    tags=['Record', 'Medium'],
)
user_album_router = APIRouter(
    prefix='/api/user-albums',
    dependencies=[Depends(require_auth)],
    tags=['Record', 'User Album'],
)


# Album work routes


@album_work_router.post('', response_model=record_schemas.AlbumWorkRead)
def create_album_work_route(
    album_in: record_schemas.AlbumWorkCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> record_models.AlbumWork:
    """Create a new AlbumWork.

    Args:
    ----
        album_in (AlbumWorkCreate): AlbumWork data for creation.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    AlbumWork: The created AlbumWork object.

    """
    return record_crud.create_album_work(db, album_in, user.sub)


@album_work_router.get('/{album_id}', response_model=record_schemas.AlbumWorkRead)
def read_album_work_route(
    album_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> record_models.AlbumWork:
    """Get a single AlbumWork by ID.

    Args:
    ----
        album_id (UUID): The ID of the AlbumWork to retrieve.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    AlbumWork: The AlbumWork object.

    Raises:
    ------
    HTTPException: If the AlbumWork is not found.

    """
    album = record_crud.get_album_work(db, album_id)
    if not album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='AlbumWork not found')
    return album


@album_work_router.get('', response_model=list[record_schemas.AlbumWorkRead])
def read_album_works_route(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[record_models.AlbumWork]:
    """Get a paginated list of AlbumWork objects.

    Args:
    ----
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    list[AlbumWork]: List of AlbumWork objects.

    """
    return record_crud.get_album_works(db, skip=skip, limit=limit)


@album_work_router.patch('/{album_id}', response_model=record_schemas.AlbumWorkRead, response_model_exclude_unset=True)
def update_album_work_route(
    album_id: UUID,
    album_in: record_schemas.AlbumWorkUpdate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> record_models.AlbumWork:
    """Update an existing AlbumWork by ID.

    Args:
    ----
        album_id (UUID): The ID of the AlbumWork to update.
        album_in (AlbumWorkUpdate): Data to update.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    AlbumWork: The updated AlbumWork object.

    Raises:
    ------
    HTTPException: If the AlbumWork is not found.

    """
    db_obj = record_crud.get_album_work(db, album_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='AlbumWork not found')

    return record_crud.update_album_work(db, db_obj, album_in, user.sub)


@album_work_router.delete('/{album_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_album_work_route(album_id: UUID, db: Annotated[Session, Depends(get_db)]) -> Response:
    """Delete an AlbumWork by ID.

    Args:
    ----
        album_id (UUID): The ID of the AlbumWork to delete.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    Response: A response with HTTP 204 status indicating successful deletion.

    Raises:
    ------
    HTTPException: If the AlbumWork is not found.

    """
    db_obj = record_crud.get_album_work(db, album_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='AlbumWork not found')

    record_crud.delete_album_work(db, album_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Release routes


@release_router.post('', response_model=record_schemas.ReleaseRead)
def create_release_route(
    release_in: record_schemas.ReleaseCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> record_models.Release:
    """Create a new Release.

    Args:
    ----
        release_in (ReleaseCreate): Release data for creation.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    Release: The created Release object.

    """
    return record_crud.create_release(db, release_in, user.sub)


@release_router.get('/{release_id}', response_model=record_schemas.ReleaseRead)
def read_release_route(release_id: UUID, db: Annotated[Session, Depends(get_db)]) -> record_models.Release:
    """Get a single Release by ID.

    Args:
    ----
        release_id (UUID): The ID of the Release to retrieve.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    Release: The Release object.

    Raises:
    ------
    HTTPException: If the Release is not found.

    """
    release = record_crud.get_release(db, release_id)
    if not release:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Release not found')
    return release


@release_router.get('', response_model=list[record_schemas.ReleaseRead])
def read_releases_route(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[record_models.Release]:
    """Get a paginated list of Release objects.

    Args:
    ----
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    list[Release]: List of Release objects.

    """
    return record_crud.get_releases(db, skip=skip, limit=limit)


@release_router.patch('/{release_id}', response_model=record_schemas.ReleaseRead, response_model_exclude_unset=True)
def update_release_route(
    release_id: UUID,
    release_in: record_schemas.ReleaseUpdate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> record_models.Release:
    """Update an existing Release by ID.

    Args:
    ----
        release_id (UUID): The ID of the Release to update.
        release_in (ReleaseUpdate): Data to update.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    Release: The updated Release object.

    Raises:
    ------
    HTTPException: If the Release is not found.

    """
    db_obj = record_crud.get_release(db, release_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Release not found')

    return record_crud.update_release(db, db_obj, release_in, user.sub)


@release_router.delete('/{release_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_release_route(release_id: UUID, db: Annotated[Session, Depends(get_db)]) -> Response:
    """Delete an Release by ID.

    Args:
    ----
        release_id (UUID): The ID of the Release to delete.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    Response: A response with HTTP 204 status indicating successful deletion.

    Raises:
    ------
    HTTPException: If the Release is not found.

    """
    db_obj = record_crud.get_release(db, release_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Release not found')

    record_crud.delete_release(db, release_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Medium routes


@medium_router.post('', response_model=record_schemas.MediumRead)
def create_medium_route(
    medium_in: record_schemas.MediumCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> record_models.Medium:
    """Create a new Medium.

    Args:
    ----
        medium_in (MediumCreate): Medium data for creation.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    Medium: The created Medium object.

    """
    return record_crud.create_medium(db, medium_in, user.sub)


@medium_router.get('/{medium_id}', response_model=record_schemas.MediumRead)
def read_medium_route(medium_id: UUID, db: Annotated[Session, Depends(get_db)]) -> record_models.Medium:
    """Get a single Medium by ID.

    Args:
    ----
        medium_id (UUID): The ID of the Medium to retrieve.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    Medium: The Medium object.

    Raises:
    ------
    HTTPException: If the Medium is not found.

    """
    medium = record_crud.get_medium(db, medium_id)
    if not medium:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Medium not found')
    return medium


@medium_router.get('', response_model=list[record_schemas.MediumRead])
def read_mediums_route(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[record_models.Medium]:
    """Get a paginated list of Medium objects.

    Args:
    ----
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    list[Medium]: List of Medium objects.

    """
    return record_crud.get_mediums(db, skip=skip, limit=limit)


@medium_router.patch('/{medium_id}', response_model=record_schemas.MediumRead, response_model_exclude_unset=True)
def update_medium_route(
    medium_id: UUID,
    medium_in: record_schemas.MediumUpdate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> record_models.Medium:
    """Update an existing Medium by ID.

    Args:
    ----
        medium_id (UUID): The ID of the Medium to update.
        medium_in (MediumUpdate): Data to update.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    Medium: The updated Medium object.

    Raises:
    ------
    HTTPException: If the Medium is not found.

    """
    db_obj = record_crud.get_medium(db, medium_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Medium not found')

    return record_crud.update_medium(db, db_obj, medium_in, user.sub)


@medium_router.delete('/{medium_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_medium_route(medium_id: UUID, db: Annotated[Session, Depends(get_db)]) -> Response:
    """Delete a Medium by ID.

    Args:
    ----
        medium_id (UUID): The ID of the Medium to delete.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    Response: A response with HTTP 204 status indicating successful deletion.

    Raises:
    ------
    HTTPException: If the Medium is not found.

    """
    db_obj = record_crud.get_medium(db, medium_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Medium not found')

    record_crud.delete_medium(db, medium_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UserAlbum routes


@user_album_router.post('', response_model=record_schemas.UserAlbumRead)
def create_user_album_route(
    user_album_in: record_schemas.UserAlbumCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> record_models.UserAlbum:
    """Create a new UserAlbum.

    Args:
    ----
        user_album_in (UserAlbumCreate): UserAlbum data for creation.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    UserAlbum: The created UserAlbum object.

    """
    return record_crud.create_user_album(db, user_album_in, user.sub)


@user_album_router.get('/{user_album_id}', response_model=record_schemas.UserAlbumRead)
def read_user_album_route(user_album_id: UUID, db: Annotated[Session, Depends(get_db)]) -> record_models.UserAlbum:
    """Get a single UserAlbum by ID.

    Args:
    ----
        user_album_id (UUID): The ID of the UserAlbum to retrieve.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    UserAlbum: The UserAlbum object.

    Raises:
    ------
    HTTPException: If the UserAlbum is not found.

    """
    user_album = record_crud.get_user_album(db, user_album_id)
    if not user_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='UserAlbum not found')
    return user_album


@user_album_router.get('', response_model=list[record_schemas.UserAlbumRead])
def read_user_albums_route(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[record_models.UserAlbum]:
    """Get a paginated list of UserAlbum objects.

    Args:
    ----
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    list[UserAlbum]: List of UserAlbum objects.

    """
    return record_crud.get_user_albums(db, skip=skip, limit=limit)


@user_album_router.patch(
    '/{user_album_id}', response_model=record_schemas.UserAlbumRead, response_model_exclude_unset=True
)
def update_user_album_route(
    user_album_id: UUID,
    user_album_in: record_schemas.UserAlbumUpdate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> record_models.UserAlbum:
    """Update an existing UserAlbum by ID.

    Args:
    ----
        user_album_id (UUID): The ID of the UserAlbum to update.
        user_album_in (UserAlbumUpdate): Data to update.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    UserAlbum: The updated UserAlbum object.

    Raises:
    ------
    HTTPException: If the UserAlbum is not found.

    """
    db_obj = record_crud.get_user_album(db, user_album_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='UserAlbum not found')
    return record_crud.update_user_album(db, db_obj, user_album_in)


@user_album_router.delete('/{user_album_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user_album_route(user_album_id: UUID, db: Annotated[Session, Depends(get_db)]) -> Response:
    """Delete a UserAlbum by ID.

    Args:
    ----
        user_album_id (UUID): The ID of the UserAlbum to delete.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    Response: A response with HTTP 204 status indicating successful deletion.

    Raises:
    ------
    HTTPException: If the UserAlbum is not found.

    """
    db_obj = record_crud.get_user_album(db, user_album_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='UserAlbum not found')

    record_crud.delete_user_album(db, user_album_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
