"""User-related API endpoints.

Includes authenticated user profile endpoints such as /me.
"""

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from shelf.app.dependencies import (
    require_auth,
    get_token_payload,
)
from shelf.app.schemas.auth import TokenPayload


user_router = APIRouter(
    prefix="/api",
    dependencies=[Depends(require_auth)],
    tags=["Shelf", "User"],
)


@user_router.get("/me")
def get_me(
    payload: Annotated[TokenPayload, Depends(get_token_payload)]
):
    """Return current authenticated user profile in Shelf context."""
    return {
        "user_id": payload.sub,
        "email": payload.email,
    }
