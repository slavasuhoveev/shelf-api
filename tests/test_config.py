import importlib


def test_postgres_url_parsing(monkeypatch):
    monkeypatch.setenv('POSTGRES_USER', 'user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'pass')
    monkeypatch.setenv('POSTGRES_DB', 'db')
    monkeypatch.setenv('POSTGRES_HOST', 'host')
    monkeypatch.setenv('POSTGRES_PORT', '1234')

    config = importlib.reload(importlib.import_module('shelf.app.core.config'))

    assert config.settings.postgres_url == 'postgresql://user:pass@host:1234/db'
