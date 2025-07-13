import pytest

valid_data = {
    'title': 't',
    'artist': 'a',
    'year_composed': 2000,
    'genre': 'g',
    'style': 's',
    'tracks': ['t1'],
}

invalid_data = {**valid_data, 'year_composed': 1800}

@pytest.mark.parametrize('payload,expected_status', [
    pytest.param(valid_data, 200, id='valid'),
    pytest.param(invalid_data, 422, id='invalid'),
])
def test_create_album_work(client, payload, expected_status):
    response = client.post('/album_work/', json=payload)
    assert response.status_code == expected_status
