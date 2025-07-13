import pytest
from pydantic import ValidationError
from uuid import uuid4

from shelf.app.schemas.record import (
    AlbumWorkCreate,
    ReleaseCreate,
    MediumCreate,
    UserAlbumCreate,
)
from shelf.app.schemas.shelf import (
    StorageSlotCreate,
    StorageItemCreate,
    StorageGroupCreate,
)
from shelf.app.enums.record import MediumFormat
from shelf.app.enums.shelf import StorageType

valid_album = {
    'title': 't',
    'artist': 'a',
    'year_composed': 2000,
    'genre': 'g',
    'style': 's',
    'tracks': ['t1'],
}

invalid_album = {**valid_album, 'year_composed': 1800}

valid_release = {
    'album_work_id': uuid4(),
    'label': 'l',
    'country': 'c',
    'year': 2000,
    'tracklist': ['a'],
    'notes': None,
}

invalid_release = {**valid_release, 'year': 1800}

valid_medium = {
    'release_id': uuid4(),
    'format': MediumFormat.VINYL,
    'medium_count': 1,
    'sides': [{}],
    'color_hint': 'red',
}

invalid_medium = {**valid_medium, 'medium_count': 0}

valid_user_album = {
    'medium_id': uuid4(),
}

invalid_user_album = {**valid_user_album, 'vinyl_grade': 'BAD'}

valid_slot = {
    'storage_item_id': uuid4(),
    'user_album_id': uuid4(),
    'position': {},
    'capacity': 1,
}

invalid_slot = {**valid_slot, 'capacity': 0}

valid_item = {
    'group_id': uuid4(),
    'title': 'i',
    'description': 'd',
    'is_public': False,
    'storage_type': StorageType.SHELF,
    'form_vector': {},
    'position_vector': None,
}

invalid_item = {**valid_item, 'storage_type': 'invalid'}

valid_group = {
    'title': 'g',
    'description': 'd',
    'is_public': False,
}

invalid_group = {**valid_group, 'title': ''}

@pytest.mark.parametrize(
    'schema,data,should_fail',
    [
        (AlbumWorkCreate, valid_album, False),
        pytest.param(AlbumWorkCreate, invalid_album, True, id='album_invalid'),
        (ReleaseCreate, valid_release, False),
        pytest.param(ReleaseCreate, invalid_release, True, id='release_invalid'),
        (MediumCreate, valid_medium, False),
        pytest.param(MediumCreate, invalid_medium, True, id='medium_invalid'),
        (UserAlbumCreate, valid_user_album, False),
        pytest.param(UserAlbumCreate, invalid_user_album, True, id='user_album_invalid'),
        (StorageSlotCreate, valid_slot, False),
        pytest.param(StorageSlotCreate, invalid_slot, True, id='slot_invalid'),
        (StorageItemCreate, valid_item, False),
        pytest.param(StorageItemCreate, invalid_item, True, id='item_invalid'),
        (StorageGroupCreate, valid_group, False),
        pytest.param(StorageGroupCreate, invalid_group, True, id='group_invalid'),
    ]
)
def test_schema_validation(schema, data, should_fail):
    if should_fail:
        with pytest.raises(ValidationError):
            schema(**data)
    else:
        obj = schema(**data)
        assert obj
