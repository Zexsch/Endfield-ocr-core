from dataclasses import dataclass, field
from enum import Enum


class Region(str, Enum):
    VALLEY = "valley"
    WULING = "wuling"


class CropTypes(str, Enum):
    NUMBER = "crop_numbers"
    ITEM = "crop_items"


@dataclass
class Config:
    region: Region = field(default=Region.VALLEY)
    debug: bool = field(default=False)


VALLEY_ITEM_NAMES: list[str] = [
    "Ankhorillig Kitchenware",
    "Musbeast Scrimshaw Dangles",
    "Witchcraft Mining Drill",
    "Aggeloi War Tins",
    "Valley Hydroculture Fillets",
    "Unity Syrup",
    "Originium Saplings",
    "Vigilant Pickaxes",
    "Astarron Crystals",
    "Scrap Toy Blocks",
    "Hard Noggin Helmets",
    "Ses'qamam Knucklebones",
]

WULING_ITEM_NAMES: list[str] = [
    "Eureka Anti-smog Tincture",
    "Wuling Frozen Pears",
    "Wuxia Movies",
    "Nymphsprout",
]
