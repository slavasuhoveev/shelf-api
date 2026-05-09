from uuid import uuid4

import pytest
from pydantic import ValidationError

from shelf.app.enums.record import MediumFormat
from shelf.app.enums.shelf import StorageType
from shelf.app.schemas.record import AlbumWorkCreate, MediumCreate, ReleaseCreate, UserAlbumCreate
from shelf.app.schemas.shelf import StorageGroupCreate, StorageItemCreate, StorageSlotCreate


@pytest.mark.parametrize(
    ('schema_cls', 'payload', 'expect_error'),
    [
        pytest.param(
            AlbumWorkCreate,
            {'title': 'A', 'artist': 'B', 'year_composed': 1990, 'genre': 'Rock', 'style': 'Alt', 'tracks': ['T1']},
            False,
            id='album_work-valid',
        ),
        pytest.param(
            AlbumWorkCreate,
            {'title': 'A', 'artist': 'B', 'year_composed': 1800, 'genre': 'Rock', 'style': 'Alt', 'tracks': ['T1']},
            True,
            id='album_work-invalid-year',
        ),
        pytest.param(
            ReleaseCreate,
            {'album_work_id': uuid4(), 'label': 'L', 'country': 'US', 'year': 1990, 'tracklist': ['T1'], 'notes': None},
            False,
            id='release-valid',
        ),
        pytest.param(
            ReleaseCreate,
            {'album_work_id': uuid4(), 'label': 'L', 'country': 'US', 'year': 2200, 'tracklist': ['T1'], 'notes': None},
            True,
            id='release-invalid-year',
        ),
        pytest.param(
            MediumCreate,
            {
                'release_id': uuid4(),
                'format': MediumFormat.VINYL,
                'medium_count': 1,
                'sides': [{}],
                'color_hint': 'black',
            },
            False,
            id='medium-valid',
        ),
        pytest.param(
            MediumCreate,
            {
                'release_id': uuid4(),
                'format': MediumFormat.VINYL,
                'medium_count': 0,
                'sides': [{}],
                'color_hint': 'black',
            },
            True,
            id='medium-invalid-count',
        ),
        pytest.param(UserAlbumCreate, {'medium_id': uuid4(), 'is_shared': False}, False, id='user_album-valid'),
        pytest.param(
            UserAlbumCreate,
            {'medium_id': uuid4(), 'vinyl_grade': 'BAD'},
            True,
            id='user_album-invalid-grade',
        ),
        pytest.param(
            StorageGroupCreate,
            {'title': 'Living room', 'description': 'Main', 'is_public': False},
            False,
            id='storage_group-valid',
        ),
        pytest.param(
            StorageGroupCreate,
            {'description': 'Main', 'is_public': False},
            True,
            id='storage_group-missing-title',
        ),
        pytest.param(
            StorageItemCreate,
            {
                'group_id': uuid4(),
                'title': 'Shelf',
                'description': 'desc',
                'storage_type': StorageType.SHELF,
                'form_vector': {},
                'position_vector': None,
            },
            False,
            id='storage_item-valid',
        ),
        pytest.param(
            StorageItemCreate,
            {
                'group_id': uuid4(),
                'title': 'Shelf',
                'description': 'desc',
                'storage_type': 'WRONG',
                'form_vector': {},
                'position_vector': None,
            },
            True,
            id='storage_item-invalid-type',
        ),
        pytest.param(
            StorageSlotCreate,
            {'storage_item_id': uuid4(), 'user_album_id': uuid4(), 'position': {}, 'capacity': 1},
            False,
            id='storage_slot-valid',
        ),
        pytest.param(
            StorageSlotCreate,
            {'storage_item_id': uuid4(), 'user_album_id': uuid4(), 'position': {}, 'capacity': 0},
            True,
            id='storage_slot-invalid-capacity',
        ),
    ],
)
def test_schema_validation_with_valid_and_invalid_data(schema_cls, payload, expect_error):
    if expect_error:
        with pytest.raises(ValidationError):
            schema_cls(**payload)
    else:
        model = schema_cls(**payload)
        assert model
