from uuid import uuid4
import pytest

from shelf.app.models import record as rec_models
from shelf.app.models import shelf as shelf_models


def create_album_work(db):
    obj = rec_models.AlbumWork(
        title='t',
        artist='a',
        year_composed=2000,
        genre='g',
        style='s',
        tracks=['t1'],
        created_by=uuid4(),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_release(db, album):
    obj = rec_models.Release(
        album_work_id=album.id,
        year=2000,
        tracklist=['t1'],
        created_by=uuid4(),
        label=None,
        country=None,
        notes=None,
        is_public=True,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_medium(db, release):
    obj = rec_models.Medium(
        release_id=release.id,
        format=rec_models.MediumFormat.VINYL,
        medium_count=1,
        sides=[{}],
        color_hint='red',
        created_by=uuid4(),
        notes=None,
        is_public=True,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_user_album(db, medium):
    obj = rec_models.UserAlbum(
        user_id=uuid4(),
        medium_id=medium.id,
        custom_notes=None,
        custom_cover=None,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_storage_group(db):
    obj = shelf_models.StorageGroup(
        user_id=uuid4(),
        title='g',
        description='d',
        is_public=False,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_storage_item(db, group):
    obj = shelf_models.StorageItem(
        user_id=uuid4(),
        group_id=group.id,
        title='i',
        description='d',
        is_public=False,
        storage_type=shelf_models.StorageType.SHELF,
        form_vector={},
        position_vector=None,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_storage_slot(db, item, user_album):
    obj = shelf_models.StorageSlot(
        storage_item_id=item.id,
        user_album_id=user_album.id,
        position={},
        capacity=1,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@pytest.mark.parametrize(
    'creator', [
        pytest.param('album', id='AlbumWork'),
        pytest.param('release', id='Release'),
        pytest.param('medium', id='Medium'),
        pytest.param('user_album', id='UserAlbum'),
        pytest.param('storage_group', id='StorageGroup'),
        pytest.param('storage_item', id='StorageItem'),
        pytest.param('storage_slot', id='StorageSlot'),
    ]
)
def test_model_persistence_chain(db_session, creator):
    album = create_album_work(db_session)
    release = create_release(db_session, album)
    medium = create_medium(db_session, release)
    user_album = create_user_album(db_session, medium)
    group = create_storage_group(db_session)
    item = create_storage_item(db_session, group)
    slot = create_storage_slot(db_session, item, user_album)

    mapping = {
        'album': album,
        'release': release,
        'medium': medium,
        'user_album': user_album,
        'storage_group': group,
        'storage_item': item,
        'storage_slot': slot,
    }

    obj = mapping[creator]
    assert obj.id is not None
    cls = type(obj)
    assert db_session.query(cls).filter_by(id=obj.id).first() is not None
