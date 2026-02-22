"""API routes for shelf and storage endpoints."""

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

from shelf.app.schemas import shelf as shelf_schemas
from shelf.app.crud import shelf as shelf_crud
from shelf.app.schemas.auth import TokenPayload
from shelf.app.dependencies import (
    get_db,
    require_auth,
    get_token_payload,
)
from shelf.app.models import shelf as shelf_models

storage_slot_router = APIRouter(
    prefix="api/storage_slot",
    dependencies=[Depends(require_auth)],
    tags=["Shelf", "Storage Slot"],
)
storage_item_router = APIRouter(
    prefix="api/storage_item",
    dependencies=[Depends(require_auth)],
    tags=["Shelf", "Storage Item"],
)
storage_group_router = APIRouter(
    prefix="api/storage_group",
    dependencies=[Depends(require_auth)],
    tags=["Shelf", "Storage Group"],
)


# Storage Slot routs

@storage_slot_router.post("/", response_model=shelf_schemas.StorageSlotRead)
def create_storage_slot_route(
    storage_slot_in: shelf_schemas.StorageSlotCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> shelf_models.StorageSlot:
    """Create a new StorageSlot.

    Args:
    ----
        storage_slot_in (StorageSlotCreate): StorageSlot data for creation.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    StorageSlot: The created StorageSlot object.

    """
    return shelf_crud.create_storage_slot(db, storage_slot_in, user["sub"])


@storage_slot_router.get("/{storage_slot_id}", response_model=shelf_schemas.StorageSlotRead)
def read_storage_slot_route(
    storage_slot_id: UUID,
    db: Annotated[Session, Depends(get_db)]
) -> shelf_models.StorageSlot:
    """Get a single StorageSlot by ID.

    Args:
    ----
        storage_slot_id (UUID): The ID of the StorageSlot to retrieve.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    StorageSlot: The StorageSlot object.

    Raises:
    ------
    HTTPException: If the StorageSlot is not found.

    """
    storage_slot = shelf_crud.get_storage_slot(db, storage_slot_id)
    if not storage_slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="StorageSlot not found"
        )
    return storage_slot


@storage_slot_router.get("/", response_model=list[shelf_schemas.StorageSlotRead])
def read_storage_slots_route(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[shelf_models.StorageSlot]:
    """Get a paginated list of StorageSlot objects.

    Args:
    ----
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    list[StorageSlot]: List of StorageSlot objects.

    """
    return shelf_crud.get_storage_slots(db, skip=skip, limit=limit)


@storage_slot_router.patch("/{storage_slot_id}",
                         response_model=shelf_schemas.StorageSlotRead,
                         response_model_exclude_unset=True)
def update_storage_slot_route(
    storage_slot_id: UUID,
    storage_slot_in: shelf_schemas.StorageSlotUpdate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> shelf_models.StorageSlot:
    """Update an existing StorageSlot by ID.

    Args:
    ----
        storage_slot_id (UUID): The ID of the StorageSlot to update.
        storage_slot_in (StorageSlotUpdate): Data to update.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    StorageSlot: The updated StorageSlot object.

    Raises:
    ------
    HTTPException: If the StorageSlot is not found.

    """
    db_obj = shelf_crud.get_storage_slot(db, storage_slot_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="StorageSlot not found"
        )

    return shelf_crud.update_storage_slot(db, db_obj, storage_slot_in, user["sub"])


@storage_slot_router.delete("/{storage_slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_storage_slot_route(
    storage_slot_id: UUID,
    db: Annotated[Session, Depends(get_db)]
) -> Response:
    """Delete a StorageSlot by ID.

    Args:
    ----
        storage_slot_id (UUID): The ID of the StorageSlot to delete.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    Response: A response with HTTP 204 status indicating successful deletion.

    Raises:
    ------
    HTTPException: If the StorageSlot is not found.

    """
    db_obj = shelf_crud.get_storage_slot(db, storage_slot_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="StorageSlot not found"
        )

    shelf_crud.delete_storage_slot(db, storage_slot_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Storage Item routs

@storage_item_router.post("/", response_model=shelf_schemas.StorageItemRead)
def create_storage_item_route(
    storage_item_in: shelf_schemas.StorageItemCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> shelf_models.StorageItem:
    """Create a new StorageItem.

    Args:
    ----
        storage_item_in (StorageItemCreate): StorageItem data for creation.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    StorageItem: The created StorageItem object.

    """
    return shelf_crud.create_storage_item(db, storage_item_in, user["sub"])


@storage_item_router.get("/{storage_item_id}", response_model=shelf_schemas.StorageItemRead)
def read_storage_item_route(
    storage_item_id: UUID,
    db: Annotated[Session, Depends(get_db)]
) -> shelf_models.StorageItem:
    """Get a single StorageItem by ID.

    Args:
    ----
        storage_item_id (UUID): The ID of the StorageItem to retrieve.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    StorageItem: The StorageItem object.

    Raises:
    ------
    HTTPException: If the StorageItem is not found.

    """
    album = shelf_crud.get_storage_item(db, storage_item_id)
    if not album:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="StorageItem not found"
        )
    return album


@storage_item_router.get("/", response_model=list[shelf_schemas.StorageItemRead])
def read_storage_items_route(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[shelf_models.StorageItem]:
    """Get a paginated list of StorageItem objects.

    Args:
    ----
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    list[StorageItem]: List of StorageItem objects.

    """
    return shelf_crud.get_storage_items(db, skip=skip, limit=limit)


@storage_item_router.patch("/{storage_item_id}",
                         response_model=shelf_schemas.StorageItemRead,
                         response_model_exclude_unset=True)
def update_storage_item_route(
    storage_item_id: UUID,
    storage_item_in: shelf_schemas.StorageItemUpdate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> shelf_models.StorageItem:
    """Update an existing StorageItem by ID.

    Args:
    ----
        storage_item_id (UUID): The ID of the StorageItem to update.
        storage_item_in (StorageItemUpdate): Data to update.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    StorageItem: The updated StorageItem object.

    Raises:
    ------
    HTTPException: If the StorageItem is not found.

    """
    db_obj = shelf_crud.get_storage_item(db, storage_item_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="StorageItem not found"
        )

    return shelf_crud.update_storage_item(db, db_obj, storage_item_in, user["sub"])


@storage_item_router.delete("/{storage_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_storage_item_route(
    storage_item_id: UUID,
    db: Annotated[Session, Depends(get_db)]
) -> Response:
    """Delete a StorageItem by ID.

    Args:
    ----
        storage_item_id (UUID): The ID of the StorageItem to delete.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    Response: A response with HTTP 204 status indicating successful deletion.

    Raises:
    ------
    HTTPException: If the StorageItem is not found.

    """
    db_obj = shelf_crud.get_storage_item(db, storage_item_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="StorageItem not found"
        )

    shelf_crud.delete_storage_item(db, storage_item_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Storage Group routs

@storage_group_router.post("/", response_model=shelf_schemas.StorageGroupRead)
def create_storage_group_route(
    storage_group_in: shelf_schemas.StorageGroupCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> shelf_models.StorageGroup:
    """Create a new StorageGroup.

    Args:
    ----
        storage_group_in (StorageGroupCreate): StorageGroup data for creation.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    StorageGroup: The created StorageGroup object.

    """
    return shelf_crud.create_storage_group(db, storage_group_in, user["sub"])


@storage_group_router.get("/{storage_group_id}", response_model=shelf_schemas.StorageGroupRead)
def read_storage_group_route(
    storage_group_id: UUID,
    db: Annotated[Session, Depends(get_db)]
) -> shelf_models.StorageGroup:
    """Get a single StorageGroup by ID.

    Args:
    ----
        storage_group_id (UUID): The ID of the StorageGroup to retrieve.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    StorageGroup: The StorageGroup object.

    Raises:
    ------
    HTTPException: If the StorageGroup is not found.

    """
    storage_group = shelf_crud.get_storage_group(db, storage_group_id)
    if not storage_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="StorageGroup not found"
        )
    return storage_group


@storage_group_router.get("/", response_model=list[shelf_schemas.StorageGroupRead])
def read_storage_groups_route(
    db: Annotated[Session, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[shelf_models.StorageGroup]:
    """Get a paginated list of StorageGroup objects.

    Args:
    ----
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    list[StorageGroup]: List of StorageGroup objects.

    """
    return shelf_crud.get_storage_groups(db, skip=skip, limit=limit)


@storage_group_router.patch("/{storage_group_id}",
                         response_model=shelf_schemas.StorageGroupRead,
                         response_model_exclude_unset=True)
def update_storage_group_route(
    storage_group_id: UUID,
    storage_group_in: shelf_schemas.StorageGroupUpdate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[TokenPayload, Depends(get_token_payload)],
) -> shelf_models.StorageGroup:
    """Update an existing StorageGroup by ID.

    Args:
    ----
        storage_group_id (UUID): The ID of the StorageGroup to update.
        storage_group_in (StorageGroupUpdate): Data to update.
        db (Session): SQLAlchemy session dependency.
        user (TokenPayload): The authenticated user information.

    Returns:
    -------
    StorageGroup: The updated StorageGroup object.

    Raises:
    ------
    HTTPException: If the StorageGroup is not found.

    """
    db_obj = shelf_crud.get_storage_group(db, storage_group_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="StorageGroup not found"
        )

    return shelf_crud.update_storage_group(db, db_obj, storage_group_in, user["sub"])


@storage_group_router.delete("/{storage_group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_storage_group_route(
    storage_group_id: UUID,
    db: Annotated[Session, Depends(get_db)]
) -> Response:
    """Delete a StorageGroup by ID.

    Args:
    ----
        storage_group_id (UUID): The ID of the StorageGroup to delete.
        db (Session): SQLAlchemy session dependency.

    Returns:
    -------
    Response: A response with HTTP 204 status indicating successful deletion.

    Raises:
    ------
    HTTPException: If the StorageGroup is not found.

    """
    db_obj = shelf_crud.get_storage_group(db, storage_group_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="StorageGroup not found"
        )

    shelf_crud.delete_storage_group(db, storage_group_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
