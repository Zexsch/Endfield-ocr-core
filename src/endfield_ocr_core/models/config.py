from dataclasses import dataclass, field
from enum import Enum

class Region(str, Enum):
    VALLEY = "valley"
    WULING = "wuling"

@dataclass
class Config:
    region: Region = field(default=Region.VALLEY)
    debug: bool = field(default=False)