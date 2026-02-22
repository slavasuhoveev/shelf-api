from uuid import uuid4

from shelf.app.enums.record import MediumFormat
from shelf.app.enums.shelf import StorageType


def album_payload(**overrides):
    payload = {
        'title': 'Kind of Blue',
        'artist': 'Miles Davis',
        'year_composed': 1959,
        'genre': 'Jazz',
        'style': 'Modal',
        'tracks': ['So What'],
        'notes': 'Classic',
        'is_public': False,
    }
    payload.update(overrides)
    return payload


def release_payload(album_work_id, **overrides):
    payload = {
        'album_work_id': str(album_work_id),
        'label': 'Columbia',
        'country': 'US',
        'year': 1959,
        'tracklist': ['So What'],
        'notes': None,
        'is_public': False,
    }
    payload.update(overrides)
    return payload


def medium_payload(release_id, **overrides):
    payload = {
        'release_id': str(release_id),
        'format': MediumFormat.VINYL.value,
        'medium_count': 1,
        'sides': [{'a': ['So What']}],
        'color_hint': 'black',
        'notes': None,
        'is_public': False,
    }
    payload.update(overrides)
    return payload


def user_album_payload(medium_id, **overrides):
    payload = {
        'medium_id': str(medium_id),
        'custom_notes': None,
        'custom_cover': None,
        'vinyl_grade': None,
        'sleeve_grade': None,
        'is_shared': False,
    }
    payload.update(overrides)
    return payload


def storage_group_payload(**overrides):
    payload = {
        'title': 'Living room',
        'description': 'Main shelf',
        'is_public': False,
    }
    payload.update(overrides)
    return payload


def storage_item_payload(group_id, **overrides):
    payload = {
        'group_id': str(group_id),
        'title': 'IKEA shelf',
        'description': '4x4',
        'is_public': False,
        'storage_type': StorageType.SHELF.value,
        'form_vector': {'w': 4, 'h': 4},
        'position_vector': {'x': 0, 'y': 0},
    }
    payload.update(overrides)
    return payload


def storage_slot_payload(storage_item_id, user_album_id, **overrides):
    payload = {
        'storage_item_id': str(storage_item_id),
        'user_album_id': str(user_album_id),
        'position': {'row': 1, 'col': 1},
        'capacity': 1,
    }
    payload.update(overrides)
    return payload


def unknown_uuid_str() -> str:
    return str(uuid4())
