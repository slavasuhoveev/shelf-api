"""CRUD operations for shelf and storage models."""

from sqlalchemy.orm import Session
from shelf.app.models.shelf import (
    StorageSlot,
    StorageItem,
    StorageGroup,
)
from shelf.app.schemas.shelf import (
    StorageSlotCreate,
    StorageSlotUpdate,
    StorageItemCreate,
    StorageItemUpdate,
    StorageGroupCreate,
    StorageGroupUpdate,
)
from uuid import UUID


# StorageSlot model crud


def create_storage_slot(
    db: Session,
    storage_slot_in: StorageSlotCreate,
) -> StorageSlot:
    """Create a new StorageSlot record in the database.

    Args:
    ----
        db (Session): SQLAlchemy session.
        storage_slot_in (StorageSlotCreate): Pydantic input with fields to create.

    Returns:
    -------
        StorageSlot: the created StorageSlot ORM object.

    """
    obj = StorageSlot(
        storage_item_id=storage_slot_in.storage_item_id,
        user_album_id=storage_slot_in.user_album_id,
        position=storage_slot_in.position,
        capacity=storage_slot_in.capacity,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_storage_slot(db: Session, storage_slot_id: UUID) -> StorageSlot | None:
    """Retrieve a single StorageSlot by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        storage_slot_id (UUID): storage slot ID.

    Returns:
    -------
        StorageSlot | None: the found StorageSlot object or None.

    """
    return db.query(StorageSlot).filter(StorageSlot.id == storage_slot_id).first()


def get_storage_slots(db: Session, skip: int = 0, limit: int = 100) -> list[StorageSlot]:
    """Retrieve a list of StorageSlot records with pagination.

    Args:
    ----
        db (Session): SQLAlchemy session.
        skip (int): number of records to skip.
        limit (int): max number of records to return.

    Returns:
    -------
        list[StorageSlot]: list of StorageSlot ORM objects.

    """
    return db.query(StorageSlot).offset(skip).limit(limit).all()


def update_storage_slot(
    db: Session,
    db_obj: StorageSlot,
    storage_slot_in: StorageSlotUpdate,
) -> StorageSlot:
    """Update an existing StorageSlot record partially.

    Args:
    ----
        db (Session): SQLAlchemy session.
        db_obj (StorageSlot): existing ORM object.
        storage_slot_in (StorageSlotUpdate): Pydantic input with fields to update.

    Returns:
    -------
        StorageSlot: updated StorageSlot ORM object.

    """
    data = storage_slot_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_storage_slot(db: Session, storage_slot_id: UUID) -> None:
    """Delete a StorageSlot object by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        storage_slot_id (UUID): storage slot ID to delete.

    Returns:
    -------
        None

    """
    obj = db.query(StorageSlot).filter(StorageSlot.id == storage_slot_id).first()
    if obj:
        db.delete(obj)
        db.commit()


# StorageItem model crud


def create_storage_item(
    db: Session,
    storage_item_in: StorageItemCreate,
    user_id: UUID,
) -> StorageItem:
    """Create a new StorageItem record in the database.

    Args:
    ----
        db (Session): SQLAlchemy session.
        storage_item_in (StorageItemCreate): Pydantic input with fields to create.
        user_id (UUID): user ID performing the storage item creation.

    Returns:
    -------
        StorageItem: the created StorageItem ORM object.

    """
    obj = StorageItem(
        user_id=user_id,
        group_id=storage_item_in.group_id,
        title=storage_item_in.title,
        description=storage_item_in.description,
        is_public=storage_item_in.is_public,
        storage_type=storage_item_in.storage_type,
        form_vector=storage_item_in.form_vector,
        position_vector=storage_item_in.position_vector,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_storage_item(db: Session, storage_item_id: UUID) -> StorageItem | None:
    """Retrieve a single StorageItem by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        storage_item_id (UUID): storage item ID.

    Returns:
    -------
        StorageItem | None: the found StorageItem object or None.

    """
    return db.query(StorageItem).filter(StorageItem.id == storage_item_id).first()


def get_storage_items(db: Session, skip: int = 0, limit: int = 100) -> list[StorageItem]:
    """Retrieve a list of StorageItem records with pagination.

    Args:
    ----
        db (Session): SQLAlchemy session.
        skip (int): number of records to skip.
        limit (int): max number of records to return.

    Returns:
    -------
        list[StorageItem]: list of StorageItem ORM objects.

    """
    return db.query(StorageItem).offset(skip).limit(limit).all()


def update_storage_item(
    db: Session,
    db_obj: StorageItem,
    storage_item_in: StorageItemUpdate,
) -> StorageItem:
    """Update an existing StorageItem record partially.

    Args:
    ----
        db (Session): SQLAlchemy session.
        db_obj (StorageItem): existing ORM object.
        storage_item_in (StorageItemUpdate): Pydantic input with fields to update.

    Returns:
    -------
        StorageItem: updated StorageItem ORM object.

    """
    data = storage_item_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_storage_item(db: Session, storage_item_id: UUID) -> None:
    """Delete a StorageItem object by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        storage_item_id (UUID): storage item ID to delete.

    Returns:
    -------
        None

    """
    obj = db.query(StorageItem).filter(StorageItem.id == storage_item_id).first()
    if obj:
        db.delete(obj)
        db.commit()


# StorageGroup model crud


def create_storage_group(
    db: Session,
    storage_group_in: StorageGroupCreate,
    user_id: UUID,
) -> StorageGroup:
    """Create a new StorageGroup record in the database.

    Args:
    ----
        db (Session): SQLAlchemy session.
        storage_group_in (StorageGroupCreate): Pydantic input with fields to create.
        user_id (UUID): user ID performing the storage group creation.

    Returns:
    -------
        StorageGroup: the created StorageGroup ORM object.

    """
    obj = StorageGroup(
        user_id=user_id,
        title=storage_group_in.title,
        description=storage_group_in.description,
        is_public=storage_group_in.is_public,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_storage_group(db: Session, storage_group_id: UUID) -> StorageGroup | None:
    """Retrieve a single StorageGroup by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        storage_group_id (UUID): storage group ID.

    Returns:
    -------
        StorageGroup | None: the found StorageGroup object or None.

    """
    return db.query(StorageGroup).filter(StorageGroup.id == storage_group_id).first()


def get_storage_groups(db: Session, skip: int = 0, limit: int = 100) -> list[StorageGroup]:
    """Retrieve a list of StorageGroup records with pagination.

    Args:
    ----
        db (Session): SQLAlchemy session.
        skip (int): number of records to skip.
        limit (int): max number of records to return.

    Returns:
    -------
        list[StorageGroup]: list of StorageGroup ORM objects.

    """
    return db.query(StorageGroup).offset(skip).limit(limit).all()


def update_storage_group(
    db: Session,
    db_obj: StorageGroup,
    storage_group_in: StorageGroupUpdate,
) -> StorageGroup:
    """Update an existing StorageGroup record partially.

    Args:
    ----
        db (Session): SQLAlchemy session.
        db_obj (StorageGroup): existing ORM object.
        storage_group_in (StorageGroupUpdate): Pydantic input with fields to update.

    Returns:
    -------
        StorageGroup: updated StorageGroup ORM object.

    """
    data = storage_group_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_storage_group(db: Session, storage_group_id: UUID) -> None:
    """Delete a StorageGroup object by its ID.

    Args:
    ----
        db (Session): SQLAlchemy session.
        storage_group_id (UUID): storage group ID to delete.

    Returns:
    -------
        None

    """
    obj = db.query(StorageGroup).filter(StorageGroup.id == storage_group_id).first()
    if obj:
        db.delete(obj)
        db.commit()
