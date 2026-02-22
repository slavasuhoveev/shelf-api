"""Application-level custom exceptions."""


class ShelfError(Exception):
    """Base application exception."""


class JWKSKeyNotFoundError(ShelfError):
    """Raised when JWT key with given kid is not found in JWKS."""


class JWKSFetchError(ShelfError):
    """Raised when JWKS cannot be fetched from Auth service."""


class InvalidTokenError(ShelfError):
    """Raised when JWT token validation fails."""
