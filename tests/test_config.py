import importlib
import os


def test_postgres_url_parsing(monkeypatch):
    monkeypatch.setenv('POSTGRES_USER', 'user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'pass')
    monkeypatch.setenv('POSTGRES_DB', 'db')
    monkeypatch.setenv('POSTGRES_HOST', 'host')
    monkeypatch.setenv('POSTGRES_PORT', '1234')
    config = importlib.reload(importlib.import_module('shelf.app.core.config'))
    assert config.POSTGRES_URL == 'postgresql://user:pass@host:1234/db'
