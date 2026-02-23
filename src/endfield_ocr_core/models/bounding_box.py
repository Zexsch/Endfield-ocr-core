from dataclasses import dataclass


@dataclass
class BoundingBox:
    """
    All values are supposed to be in percentages
    """

    x: float
    y: float
    width: float
    height: float


@dataclass
class BoundingBoxRaw:
    """
    All values are supposed to be in pixels
    """

    x: int
    y: int
    width: int
    height: int
