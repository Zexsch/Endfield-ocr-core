from rapidfuzz import process, fuzz

from endfield_ocr_core.models.exceptions import ItemNotFoundException
from endfield_ocr_core.models.config import (
    Region,
    WULING_ITEM_NAMES,
    VALLEY_ITEM_NAMES,
)


def clean_item_name(res_item: str, region: str) -> tuple[str, float]:
    res_item = res_item.replace(r"\n", "")

    if "[pkg]" in res_item:
        res_item = res_item.replace("[pkg]", "")

    if region == Region.WULING.value:
        region_item_type = WULING_ITEM_NAMES
    elif region == Region.VALLEY.value:
        region_item_type = VALLEY_ITEM_NAMES
    else:
        region_item_type = ""

    item_result = process.extractOne(res_item, region_item_type, scorer=fuzz.WRatio)

    if item_result is None:
        raise ItemNotFoundException(res_item)

    match, score, _ = item_result

    return match, score
