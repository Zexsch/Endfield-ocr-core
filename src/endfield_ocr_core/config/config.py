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
    manual: bool = field(default=False)
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

CONFIG_ITEMS = r"""
--oem 3 --psm 6 
-c preserve_interword_spaces=1 
-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789[]'-
"""

CONFIG_NUMBERS = r"""
--oem 3 --psm 8 
-c tessedit_char_whitelist=0123456789 
-c classify_bln_numeric_mode=1 
-c load_system_dawg=0 
-c load_freq_dawg=0 
-c load_punc_dawg=0 
-c load_number_dawg=1 
-c tessedit_enable_doc_dict=0
-c textord_heavy_nr=1
-c textord_min_linesize=2.5
"""

CONFIG_CROP_TOP = r"""
--psm 6
"""
