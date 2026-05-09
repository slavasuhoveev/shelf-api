from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from shelf.app.crud import record as record_crud
from shelf.app.crud import shelf as shelf_crud
from shelf.app.enums.record import MediumFormat
from shelf.app.enums.shelf import StorageType
from shelf.app.schemas.record import (
    AlbumWorkCreate,
    AlbumWorkUpdate,
    MediumCreate,
    MediumUpdate,
    ReleaseCreate,
    ReleaseUpdate,
    UserAlbumCreate,
    UserAlbumUpdate,
)
from shelf.app.schemas.shelf import (
    StorageGroupCreate,
    StorageGroupUpdate,
    StorageItemCreate,
    StorageItemUpdate,
    StorageSlotCreate,
    StorageSlotUpdate,
)


def create_chain(db_session):
    user_id = uuid4()
    album = record_crud.create_album_work(
        db_session,
        AlbumWorkCreate(
            title='A',
            artist='B',
            year_composed=1990,
            genre='Rock',
            style='Alt',
            tracks=['T1'],
        ),
        user_id,
    )
    release = record_crud.create_release(
        db_session,
        ReleaseCreate(
            album_work_id=album.id,
            label='L',
            country='US',
            year=1990,
            tracklist=['T1'],
            notes=None,
        ),
        user_id,
    )
    medium = record_crud.create_medium(
        db_session,
        MediumCreate(
            release_id=release.id,
            format=MediumFormat.VINYL,
            medium_count=1,
            sides=[{}],
            color_hint='black',
        ),
        user_id,
    )
    user_album = record_crud.create_user_album(db_session, UserAlbumCreate(medium_id=medium.id), user_id)
    group = shelf_crud.create_storage_group(
        db_session,
        StorageGroupCreate(title='Group', description='Main', is_public=False),
        user_id,
    )
    item = shelf_crud.create_storage_item(
        db_session,
        StorageItemCreate(
            group_id=group.id,
            title='Item',
            description='desc',
            storage_type=StorageType.SHELF,
            form_vector={},
            position_vector=None,
        ),
        user_id,
    )
    slot = shelf_crud.create_storage_slot(
        db_session,
        StorageSlotCreate(
            storage_item_id=item.id,
            user_album_id=user_album.id,
            position={},
            capacity=1,
        ),
    )
    return album, release, medium, user_album, group, item, slot


@pytest.mark.parametrize(
    ('name', 'getter', 'lister'),
    [
        pytest.param('album', record_crud.get_album_work, record_crud.get_album_works, id='album'),
        pytest.param('release', record_crud.get_release, record_crud.get_releases, id='release'),
        pytest.param('medium', record_crud.get_medium, record_crud.get_mediums, id='medium'),
        pytest.param('user_album', record_crud.get_user_album, record_crud.get_user_albums, id='user_album'),
        pytest.param('group', shelf_crud.get_storage_group, shelf_crud.get_storage_groups, id='storage_group'),
        pytest.param('item', shelf_crud.get_storage_item, shelf_crud.get_storage_items, id='storage_item'),
        pytest.param('slot', shelf_crud.get_storage_slot, shelf_crud.get_storage_slots, id='storage_slot'),
    ],
)
def test_crud_get_and_list(db_session, name, getter, lister):
    album, release, medium, user_album, group, item, slot = create_chain(db_session)
    mapping = {
        'album': album.id,
        'release': release.id,
        'medium': medium.id,
        'user_album': user_album.id,
        'group': group.id,
        'item': item.id,
        'slot': slot.id,
    }
    object_id = mapping[name]

    assert getter(db_session, object_id) is not None
    listed_ids = {obj.id for obj in lister(db_session)}
    assert object_id in listed_ids


@pytest.mark.parametrize(
    ('name', 'updater', 'update_schema', 'field', 'value'),
    [
        pytest.param('album', record_crud.update_album_work, AlbumWorkUpdate, 'title', 'Updated', id='album'),
        pytest.param('release', record_crud.update_release, ReleaseUpdate, 'label', 'Updated', id='release'),
        pytest.param('medium', record_crud.update_medium, MediumUpdate, 'color_hint', 'white', id='medium'),
        pytest.param(
            'user_album',
            record_crud.update_user_album,
            UserAlbumUpdate,
            'custom_notes',
            'Updated',
            id='user_album',
        ),
        pytest.param(
            'group',
            shelf_crud.update_storage_group,
            StorageGroupUpdate,
            'title',
            'Updated',
            id='storage_group',
        ),
        pytest.param('item', shelf_crud.update_storage_item, StorageItemUpdate, 'title', 'Updated', id='storage_item'),
        pytest.param('slot', shelf_crud.update_storage_slot, StorageSlotUpdate, 'capacity', 2, id='storage_slot'),
    ],
)
def test_crud_update(db_session, name, updater, update_schema, field, value):
    album, release, medium, user_album, group, item, slot = create_chain(db_session)
    mapping = {
        'album': album,
        'release': release,
        'medium': medium,
        'user_album': user_album,
        'group': group,
        'item': item,
        'slot': slot,
    }
    obj = mapping[name]
    payload = update_schema(**{field: value})

    if name in {'album', 'release', 'medium'}:
        updated = updater(db_session, obj, payload, uuid4())
    else:
        updated = updater(db_session, obj, payload)

    assert getattr(updated, field) == value


@pytest.mark.parametrize(
    ('name', 'deleter', 'getter'),
    [
        pytest.param('album', record_crud.delete_album_work, record_crud.get_album_work, id='album'),
        pytest.param('release', record_crud.delete_release, record_crud.get_release, id='release'),
        pytest.param('medium', record_crud.delete_medium, record_crud.get_medium, id='medium'),
        pytest.param('user_album', record_crud.delete_user_album, record_crud.get_user_album, id='user_album'),
        pytest.param('group', shelf_crud.delete_storage_group, shelf_crud.get_storage_group, id='storage_group'),
        pytest.param('item', shelf_crud.delete_storage_item, shelf_crud.get_storage_item, id='storage_item'),
        pytest.param('slot', shelf_crud.delete_storage_slot, shelf_crud.get_storage_slot, id='storage_slot'),
    ],
)
def test_crud_delete(db_session, name, deleter, getter):
    album, release, medium, user_album, group, item, slot = create_chain(db_session)
    mapping = {
        'album': album.id,
        'release': release.id,
        'medium': medium.id,
        'user_album': user_album.id,
        'group': group.id,
        'item': item.id,
        'slot': slot.id,
    }
    object_id = mapping[name]

    deleter(db_session, object_id)
    assert getter(db_session, object_id) is None


def test_crud_invalid_foreign_key_raises(db_session):
    with pytest.raises(IntegrityError):
        record_crud.create_release(
            db_session,
            ReleaseCreate(
                album_work_id=uuid4(),
                label='X',
                country='US',
                year=2000,
                tracklist=['T1'],
                notes=None,
            ),
            uuid4(),
        )
