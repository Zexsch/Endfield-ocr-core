from typing import Any

import toml

from endfield_ocr_core.models.config import Region
from endfield_ocr_core.utils.package_dirs import PackageDirs
from endfield_ocr_core.models.exceptions import RegionNotFoundException


def _get_config(region: str) -> dict[str, Any]:
    if region == Region.VALLEY.value:
        config_dir = PackageDirs().valley
    elif region == Region.WULING.value:
        config_dir = PackageDirs().wuling
    else:
        raise RegionNotFoundException(region)

    with config_dir.open("r", encoding="utf-8") as f:
        config = toml.load(f)

    return config


def valley(index: int, crop: str) -> dict[str, float]:
    config = _get_config(Region.VALLEY.value)
    config = config[crop]

    if index >= 7:
        h_mult = config["row_2_height"]
        h_mult_2 = config["row_2_height_cutoff"]
    else:
        h_mult = config["row_1_height"]
        h_mult_2 = config["row_1_height_cutoff"]

    w_mult = config["width"]
    w_mult_2 = config["width_2"]

    return {
        "h_mult": h_mult,
        "h_mult_2": h_mult_2,
        "w_mult": w_mult,
        "w_mult_2": w_mult_2,
    }


def wuling(index: int, crop: str) -> dict[str, float]:
    if index >= 0:
        pass

    config = _get_config(Region.WULING.value)
    config = config[crop]

    h_mult = config["row_1_height"]
    h_mult_2 = config["row_1_height_cutoff"]
    w_mult = config["width"]
    w_mult_2 = config["width_2"]
    return {
        "h_mult": h_mult,
        "h_mult_2": h_mult_2,
        "w_mult": w_mult,
        "w_mult_2": w_mult_2,
    }
