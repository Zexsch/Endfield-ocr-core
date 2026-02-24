from typing import Any

import toml

from endfield_ocr_core import Region
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
