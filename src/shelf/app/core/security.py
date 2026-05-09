"""JWT security utilities.

Contains token verification logic, claim validation,
and signature verification using JWKS.
"""

import time
import httpx
from typing import Dict, Any
from jose import jwt
from jose import ExpiredSignatureError, JWTError
from fastapi import HTTPException

from shelf.app.core.config import settings
from shelf.app.schemas.auth import TokenPayload
from shelf.app.core.errors import InvalidTokenError


class JWKSClient:
    """Client for retrieving and caching JWKS from the Auth service.

    Provides in-memory caching of the JSON Web Key Set (JWKS)
    used to verify RS256-signed JWT access tokens.

    The cache is refreshed based on a configurable TTL
    defined by `settings.JWKS_CACHE_TTL_SECONDS`.
    """

    def __init__(self):
        """Initialize JWKS client with empty cache.

        Attributes
        ----------
            _cache: Cached JWKS dictionary or None if not yet fetched.
            _last_fetch: UNIX timestamp of the last successful JWKS fetch.

        """
        self._cache: Dict[str, Any] | None = None
        self._last_fetch: float = 0

    def get_jwks(self) -> Dict[str, Any]:
        """Return JWKS, refreshing it if TTL has expired.

        The method checks whether a cached JWKS exists and whether
        the configured TTL has not yet expired. If the cache is valid,
        it returns the cached value.

        Otherwise, it fetches the JWKS from the Auth service,
        updates the in-memory cache, and returns the fresh data.

        Returns
        -------
            Dict[str, Any]: Parsed JWKS JSON structure.

        Raises
        ------
            httpx.HTTPError: If the JWKS endpoint is unreachable
                or returns a non-successful HTTP response.

        """
        now = time.time()

        if self._cache and now - self._last_fetch < settings.JWKS_CACHE_TTL_SECONDS:
            return self._cache

        response = httpx.get(str(settings.AUTH_JWKS_URL), timeout=5)
        response.raise_for_status()

        self._cache = response.json()
        self._last_fetch = now

        return self._cache


jwks_client = JWKSClient()


def verify_access_token(token: str) -> dict:
    """Verify JWT access token and return payload."""
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get('kid')

    jwks = jwks_client.get_jwks()
    key = next((k for k in jwks['keys'] if k['kid'] == kid), None)

    if not key:
        raise InvalidTokenError

    try:
        payload_dict = jwt.decode(
            token,
            key,
            algorithms=['RS256'],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired') from None

    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token') from None

    return TokenPayload(**payload_dict)
