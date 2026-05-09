import pytest

from tests.factories import (
    album_payload,
    medium_payload,
    release_payload,
    storage_group_payload,
    storage_item_payload,
    storage_slot_payload,
    unknown_uuid_str,
    user_album_payload,
)


API_ROUTES = [
    pytest.param('/api/album-works', 'album work list should be available', id='album_work-list'),
    pytest.param('/api/releases', 'release list should be available', id='release-list'),
    pytest.param('/api/mediums', 'medium list should be available', id='medium-list'),
    pytest.param('/api/user-albums', 'user album list should be available', id='user_album-list'),
    pytest.param('/api/storage_slot', 'storage slot list should be available', id='storage_slot-list'),
    pytest.param('/api/storage_item', 'storage item list should be available', id='storage_item-list'),
    pytest.param('/api/storage_group', 'storage group list should be available', id='storage_group-list'),
]


@pytest.mark.parametrize(
    ('path', 'comment'),
    API_ROUTES,
)
def test_list_routes_return_empty_array(client, path, comment):
    response = client.get(path)
    assert comment
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize(('path', 'comment'), API_ROUTES)
def test_api_routes_require_authentication(unauthenticated_client, path, comment):
    response = unauthenticated_client.get(path)
    assert comment
    assert response.status_code == 401
    assert response.json() == {'detail': 'Missing bearer token'}


def _post_json(client, path, payload):
    response = client.post(path, json=payload)
    assert response.status_code == 200, response.text
    return response.json()


def _create_chain(client):
    album = _post_json(client, '/api/album-works', album_payload())
    release = _post_json(client, '/api/releases', release_payload(album['id']))
    medium = _post_json(client, '/api/mediums', medium_payload(release['id']))
    user_album = _post_json(client, '/api/user-albums', user_album_payload(medium['id']))
    storage_group = _post_json(client, '/api/storage_group', storage_group_payload())
    storage_item = _post_json(client, '/api/storage_item', storage_item_payload(storage_group['id']))
    storage_slot = _post_json(
        client,
        '/api/storage_slot',
        storage_slot_payload(storage_item['id'], user_album['id']),
    )
    return {
        'album_work': album,
        'release': release,
        'medium': medium,
        'user_album': user_album,
        'storage_group': storage_group,
        'storage_item': storage_item,
        'storage_slot': storage_slot,
    }


@pytest.mark.parametrize(
    ('create_path', 'valid_payload_factory', 'invalid_payload_factory'),
    [
        pytest.param(
            '/api/album-works',
            lambda ids: album_payload(),
            lambda ids: album_payload(year_composed=1800),
            id='album_work',
        ),
        pytest.param(
            '/api/releases',
            lambda ids: release_payload(ids['album_work']['id']),
            lambda ids: release_payload(ids['album_work']['id'], year=1800),
            id='release',
        ),
        pytest.param(
            '/api/mediums',
            lambda ids: medium_payload(ids['release']['id']),
            lambda ids: medium_payload(ids['release']['id'], medium_count=0),
            id='medium',
        ),
        pytest.param(
            '/api/user-albums',
            lambda ids: user_album_payload(ids['medium']['id']),
            lambda ids: user_album_payload(ids['medium']['id'], vinyl_grade='INVALID'),
            id='user_album',
        ),
        pytest.param(
            '/api/storage_group',
            lambda ids: storage_group_payload(),
            lambda ids: storage_group_payload(title=''),
            id='storage_group',
        ),
        pytest.param(
            '/api/storage_item',
            lambda ids: storage_item_payload(ids['storage_group']['id']),
            lambda ids: storage_item_payload(ids['storage_group']['id'], storage_type='INVALID'),
            id='storage_item',
        ),
        pytest.param(
            '/api/storage_slot',
            lambda ids: storage_slot_payload(ids['storage_item']['id'], ids['user_album']['id']),
            lambda ids: storage_slot_payload(ids['storage_item']['id'], ids['user_album']['id'], capacity=0),
            id='storage_slot',
        ),
    ],
)
def test_create_routes_valid_and_invalid(client, create_path, valid_payload_factory, invalid_payload_factory):
    ids = _create_chain(client)

    if create_path == '/api/storage_slot':
        extra_user_album = client.post('/api/user-albums', json=user_album_payload(ids['medium']['id'])).json()
        ids['user_album'] = extra_user_album

    valid_response = client.post(create_path, json=valid_payload_factory(ids))
    invalid_response = client.post(create_path, json=invalid_payload_factory(ids))

    assert valid_response.status_code == 200
    assert invalid_response.status_code == 422


@pytest.mark.parametrize(
    ('resource', 'base_path', 'update_payload'),
    [
        pytest.param('album_work', '/api/album-works', {'title': 'Updated title'}, id='album_work'),
        pytest.param('release', '/api/releases', {'label': 'Updated label'}, id='release'),
        pytest.param('medium', '/api/mediums', {'color_hint': 'white'}, id='medium'),
        pytest.param('user_album', '/api/user-albums', {'custom_notes': 'updated'}, id='user_album'),
        pytest.param('storage_group', '/api/storage_group', {'title': 'Updated group'}, id='storage_group'),
        pytest.param('storage_item', '/api/storage_item', {'title': 'Updated item'}, id='storage_item'),
        pytest.param('storage_slot', '/api/storage_slot', {'capacity': 2}, id='storage_slot'),
    ],
)
def test_read_update_delete_cycle_and_not_found(client, resource, base_path, update_payload):
    ids = _create_chain(client)
    resource_id = ids[resource]['id']

    read_response = client.get(f'{base_path}/{resource_id}')
    assert read_response.status_code == 200
    assert read_response.json()['id'] == resource_id

    update_response = client.patch(f'{base_path}/{resource_id}', json=update_payload)
    assert update_response.status_code == 200
    updated_payload = update_response.json()
    for field, value in update_payload.items():
        assert updated_payload[field] == value

    delete_response = client.delete(f'{base_path}/{resource_id}')
    assert delete_response.status_code == 204
    assert delete_response.content == b''

    not_found_id = unknown_uuid_str()
    assert client.get(f'{base_path}/{not_found_id}').status_code == 404
    assert client.patch(f'{base_path}/{not_found_id}', json=update_payload).status_code == 404
    assert client.delete(f'{base_path}/{not_found_id}').status_code == 404
