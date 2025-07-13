import pytest

LIST_ENDPOINTS = [
    '/album_work/',
    '/release/',
    '/medium/',
    '/user_album/',
    '/storage_slot/',
    '/storage_item/',
    '/storage_group/',
]

@pytest.mark.parametrize('path', [pytest.param(p, id=p) for p in LIST_ENDPOINTS])
def test_list_routes_empty(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == []
