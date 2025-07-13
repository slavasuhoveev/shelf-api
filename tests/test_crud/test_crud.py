from uuid import uuid4
import pytest

from shelf.app.crud import record as record_crud
from shelf.app.crud import shelf as shelf_crud
from shelf.app.schemas.record import AlbumWorkCreate, ReleaseCreate, MediumCreate, UserAlbumCreate
from shelf.app.schemas.shelf import StorageSlotCreate, StorageItemCreate, StorageGroupCreate
from shelf.app.enums.record import MediumFormat
from shelf.app.enums.shelf import StorageType


def make_album_data():
    return AlbumWorkCreate(
        title='t',
        artist='a',
        year_composed=2000,
        genre='g',
        style='s',
        tracks=['t1']
    )


def make_release_data(album_id):
    return ReleaseCreate(
        album_work_id=album_id,
        label='l',
        country='c',
        year=2000,
        tracklist=['t1'],
        notes=None,
        is_public=True,
    )


def make_medium_data(release_id):
    return MediumCreate(
        release_id=release_id,
        format=MediumFormat.VINYL,
        medium_count=1,
        sides=[{}],
        color_hint='red',
        notes=None,
        is_public=True,
    )


def make_user_album_data(medium_id):
    return UserAlbumCreate(
        medium_id=medium_id,
        slot_id=None,
        custom_notes=None,
        custom_cover=None,
        is_shared=False,
    )


def make_group_data():
    return StorageGroupCreate(title='g', description='d', is_public=False)


def make_item_data(group_id):
    return StorageItemCreate(
        group_id=group_id,
        title='i',
        description='d',
        is_public=False,
        storage_type=StorageType.SHELF,
        form_vector={},
        position_vector=None,
    )


def make_slot_data(item_id, user_album_id):
    return StorageSlotCreate(
        storage_item_id=item_id,
        user_album_id=user_album_id,
        position={},
        capacity=1,
    )


@pytest.mark.parametrize('creator', [
    pytest.param('album', id='AlbumWork'),
    pytest.param('release', id='Release'),
    pytest.param('medium', id='Medium'),
    pytest.param('user_album', id='UserAlbum'),
    pytest.param('storage_group', id='StorageGroup'),
    pytest.param('storage_item', id='StorageItem'),
    pytest.param('storage_slot', id='StorageSlot'),
])
def test_crud_create(db_session, creator):
    album = record_crud.create_album_work(db_session, make_album_data(), uuid4())
    release = record_crud.create_release(db_session, make_release_data(album.id), uuid4())
    medium = record_crud.create_medium(db_session, make_medium_data(release.id), uuid4())
    user_album = record_crud.create_user_album(db_session, make_user_album_data(medium.id), uuid4())
    group = shelf_crud.create_storage_group(db_session, make_group_data(), uuid4())
    item = shelf_crud.create_storage_item(db_session, make_item_data(group.id), uuid4())
    slot = shelf_crud.create_storage_slot(db_session, make_slot_data(item.id, user_album.id))

    mapping = {
        'album': (record_crud.get_album_work, album.id),
        'release': (record_crud.get_release, release.id),
        'medium': (record_crud.get_medium, medium.id),
        'user_album': (record_crud.get_user_album, user_album.id),
        'storage_group': (shelf_crud.get_storage_group, group.id),
        'storage_item': (shelf_crud.get_storage_item, item.id),
        'storage_slot': (shelf_crud.get_storage_slot, slot.id),
    }

    getter, obj_id = mapping[creator]
    assert getter(db_session, obj_id) is not None
