from importlib import resources
from pathlib import Path
from typing import Any

import toml

from endfield_ocr_core.models.config import Region


def _get_config(region: str) -> dict[str, Any]:
    config_dir = Path(__file__).parent / "config" / f"{region}.toml"
    with resources.open_text("endfield_ocr_core.config", str(config_dir)) as f:
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
