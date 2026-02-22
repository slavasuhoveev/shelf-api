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


@pytest.mark.parametrize(
    ('path', 'comment'),
    [
        pytest.param('/album_work/', 'album work list should be available', id='album_work-list'),
        pytest.param('/release/', 'release list should be available', id='release-list'),
        pytest.param('/medium/', 'medium list should be available', id='medium-list'),
        pytest.param('/user_album/', 'user album list should be available', id='user_album-list'),
        pytest.param('/storage_slot/', 'storage slot list should be available', id='storage_slot-list'),
        pytest.param('/storage_item/', 'storage item list should be available', id='storage_item-list'),
        pytest.param('/storage_group/', 'storage group list should be available', id='storage_group-list'),
    ],
)
def test_list_routes_return_empty_array(client, path, comment):
    response = client.get(path)
    assert comment
    assert response.status_code == 200
    assert response.json() == []


def _create_chain(client):
    album = client.post('/album_work/', json=album_payload()).json()
    release = client.post('/release/', json=release_payload(album['id'])).json()
    medium = client.post('/medium/', json=medium_payload(release['id'])).json()
    user_album = client.post('/user_album/', json=user_album_payload(medium['id'])).json()
    storage_group = client.post('/storage_group/', json=storage_group_payload()).json()
    storage_item = client.post('/storage_item/', json=storage_item_payload(storage_group['id'])).json()
    storage_slot = client.post(
        '/storage_slot/',
        json=storage_slot_payload(storage_item['id'], user_album['id']),
    ).json()
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
        pytest.param('/album_work/', lambda ids: album_payload(), lambda ids: album_payload(year_composed=1800), id='album_work'),
        pytest.param('/release/', lambda ids: release_payload(ids['album_work']['id']), lambda ids: release_payload(ids['album_work']['id'], year=1800), id='release'),
        pytest.param('/medium/', lambda ids: medium_payload(ids['release']['id']), lambda ids: medium_payload(ids['release']['id'], medium_count=0), id='medium'),
        pytest.param('/user_album/', lambda ids: user_album_payload(ids['medium']['id']), lambda ids: user_album_payload(ids['medium']['id'], vinyl_grade='INVALID'), id='user_album'),
        pytest.param('/storage_group/', lambda ids: storage_group_payload(), lambda ids: storage_group_payload(title=''), id='storage_group'),
        pytest.param('/storage_item/', lambda ids: storage_item_payload(ids['storage_group']['id']), lambda ids: storage_item_payload(ids['storage_group']['id'], storage_type='INVALID'), id='storage_item'),
        pytest.param('/storage_slot/', lambda ids: storage_slot_payload(ids['storage_item']['id'], ids['user_album']['id']), lambda ids: storage_slot_payload(ids['storage_item']['id'], ids['user_album']['id'], capacity=0), id='storage_slot'),
    ],
)
def test_create_routes_valid_and_invalid(client, create_path, valid_payload_factory, invalid_payload_factory):
    ids = _create_chain(client)

    if create_path == '/storage_slot/':
        extra_user_album = client.post('/user_album/', json=user_album_payload(ids['medium']['id'])).json()
        ids['user_album'] = extra_user_album

    valid_response = client.post(create_path, json=valid_payload_factory(ids))
    invalid_response = client.post(create_path, json=invalid_payload_factory(ids))

    assert valid_response.status_code == 200
    assert invalid_response.status_code == 422


@pytest.mark.parametrize(
    ('resource', 'base_path', 'update_payload'),
    [
        pytest.param('album_work', '/album_work', {'title': 'Updated title'}, id='album_work'),
        pytest.param('release', '/release', {'label': 'Updated label'}, id='release'),
        pytest.param('medium', '/medium', {'color_hint': 'white'}, id='medium'),
        pytest.param('user_album', '/user_album', {'custom_notes': 'updated'}, id='user_album'),
        pytest.param('storage_group', '/storage_group', {'title': 'Updated group'}, id='storage_group'),
        pytest.param('storage_item', '/storage_item', {'title': 'Updated item'}, id='storage_item'),
        pytest.param('storage_slot', '/storage_slot', {'capacity': 2}, id='storage_slot'),
    ],
)
def test_read_update_delete_cycle_and_not_found(client, resource, base_path, update_payload):
    ids = _create_chain(client)
    resource_id = ids[resource]['id']

    read_response = client.get(f'{base_path}/{resource_id}')
    assert read_response.status_code == 200

    update_response = client.patch(f'{base_path}/{resource_id}', json=update_payload)
    assert update_response.status_code == 200

    delete_response = client.delete(f'{base_path}/{resource_id}')
    assert delete_response.status_code == 204

    not_found_id = unknown_uuid_str()
    assert client.get(f'{base_path}/{not_found_id}').status_code == 404
    assert client.patch(f'{base_path}/{not_found_id}', json=update_payload).status_code == 404
    assert client.delete(f'{base_path}/{not_found_id}').status_code == 404
