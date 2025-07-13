def test_get_albums_empty(client):
    response = client.get('/album_work/')
    assert response.status_code == 200
    assert response.json() == []
