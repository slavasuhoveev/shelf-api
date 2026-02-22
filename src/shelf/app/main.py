"""Shelf API application entry point.

Initializes FastAPI app, routers, and middleware.
"""

from fastapi import FastAPI

from shelf.app.routers.system import (
    system_group_router
)

from shelf.app.routers.user import (
    user_router
)

from shelf.app.routers.record import (
    album_work_router,
    release_router,
    medium_router,
    user_album_router,
)
from shelf.app.routers.shelf import (
    storage_slot_router,
    storage_item_router,
    storage_group_router,
)

app = FastAPI()

# System routs
app.include_router(system_group_router)

# User routs
app.include_router(user_router)

# Record routs
app.include_router(album_work_router)
app.include_router(release_router)
app.include_router(medium_router)
app.include_router(user_album_router)

# Shelf routs
app.include_router(storage_slot_router)
app.include_router(storage_item_router)
app.include_router(storage_group_router)
