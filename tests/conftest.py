import os
from types import SimpleNamespace
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from shelf.app.dependencies import get_db, get_token_payload, require_auth
from shelf.app.main import app
from shelf.app.models.base import Base

TEST_DATABASE_URL = os.getenv(
    'TEST_POSTGRES_URL',
    'postgresql://shelf_user:shelf@localhost:5433/shelf_test',
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DUMMY_USER_ID = UUID('00000000-0000-0000-0000-000000000001')


@pytest.fixture(scope='session')
def db_available() -> bool:
    try:
        with engine.connect():
            return True
    except OperationalError:
        return False


@pytest.fixture(scope='session')
def setup_database(db_available: bool):
    if not db_available:
        pytest.skip('PostgreSQL test database is not available')
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(setup_database):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def unauthenticated_client():
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    def override_require_auth():
        return None

    def override_get_token_payload():
        return SimpleNamespace(sub=DUMMY_USER_ID, email='test@example.com')

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[require_auth] = override_require_auth
    app.dependency_overrides[get_token_payload] = override_get_token_payload
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
