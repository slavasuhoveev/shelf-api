from fastapi import FastAPI

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

# Record routs
app.include_router(album_work_router)
app.include_router(release_router)
app.include_router(medium_router)
app.include_router(user_album_router)

# Shelf routs
app.include_router(storage_slot_router)
app.include_router(storage_item_router)
app.include_router(storage_group_router)
