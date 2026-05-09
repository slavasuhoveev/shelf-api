"""FastAPI dependencies for authentication and request handling."""

from sqlalchemy.orm import Session
from typing import Generator
from fastapi import Request, HTTPException, status

from shelf.app.core.security import verify_access_token
from shelf.app.db.session import SessionLocal
from shelf.app.core.errors import (
    JWKSKeyNotFoundError,
    InvalidTokenError,
)


def get_db() -> Generator[Session, None, None]:
    """Yield a SQLAlchemy database session and ensure it is properly closed.

    Args:
    ----
        None

    Returns:
    -------
    Generator[Session, None, None]: a generator yielding a database session.

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_auth(request: Request) -> None:
    """Validate JWT and store payload in request.state (router guard)."""
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing bearer token')

    token = auth_header.split(' ', 1)[1].strip()

    try:
        payload = verify_access_token(token)  # returns TokenPayload (or dict)
    except (JWKSKeyNotFoundError, InvalidTokenError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired token',
        ) from None

    request.state.token_payload = payload


def get_token_payload(request: Request):
    """Return payload already validated by require_auth."""
    payload = getattr(request.state, 'token_payload', None)
    if payload is None:
        # means someone called this dependency without router guard
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    return payload
