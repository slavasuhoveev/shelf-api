"""Authentication-related Pydantic schemas.

Defines JWT token payload structures.
"""

from pydantic import BaseModel

class TokenPayload(BaseModel):
    """JWT claims we care about inside Shelf API."""

    sub: str
    email: str | None = None
    # later: roles/scopes
