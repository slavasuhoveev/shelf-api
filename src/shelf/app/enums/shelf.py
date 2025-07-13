from enum import Enum

class StorageType(str, Enum):
    """Enum for Storage types."""

    SHELF = "shelf"
    FRAME = "frame"
    STAND = "stand"
    BOX = "box"
