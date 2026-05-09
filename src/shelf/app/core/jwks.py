"""JWKS client and caching utilities.

Handles retrieval and in-memory caching of JSON Web Key Sets
from the Auth service for JWT verification.
"""

from fastapi import Request, HTTPException, status
from jose import jwt, JWTError
from shelf.app.core.config import settings
from shelf.app.core.jwks import jwks_client
from shelf.app.core.errors import JWKSKeyNotFoundError


def get_current_user(request: Request):
    """Validate JWT access token and return decoded payload."""
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = auth_header.split(' ')[1]

    try:
        # Extract kid from token header
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get('kid')

        jwks = jwks_client.get_jwks()

        key = next((k for k in jwks['keys'] if k['kid'] == kid), None)
        if not key:
            raise JWKSKeyNotFoundError

        payload = jwt.decode(
            token,
            key,
            algorithms=['RS256'],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
        )

    except JWTError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from error

    return payload
