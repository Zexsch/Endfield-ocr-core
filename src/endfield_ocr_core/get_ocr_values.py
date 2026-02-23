import pytesseract
from PIL import Image
from rapidfuzz import process, fuzz

from endfield_ocr_core.region.split_image import split_image
from endfield_ocr_core.utils.preprocess import preprocess
from endfield_ocr_core.models.exceptions import ItemNotFoundException, NotANumberException
from endfield_ocr_core.utils.debug_image_save import save_debug_image
from endfield_ocr_core.models.config import (
    CropTypes,
    Region,
    WULING_ITEM_NAMES,
    VALLEY_ITEM_NAMES,
    CONFIG_NUMBERS,
    CONFIG_ITEMS
)


def get_ocr_values(
    img: Image.Image, rows: int, cols: int, region: str, debug_files=False
) -> dict[str, int]:
    
    img_list = split_image(img, rows, cols)

    results: dict[str, int] = {}

    for index, image in enumerate(img_list):
        if region == Region.VALLEY.value and index >= 13:
            continue

        image_number = preprocess(image, index, region, CropTypes.NUMBER)
        image_item = preprocess(image, index, region, CropTypes.ITEM)
        res_number = pytesseract.image_to_string(
            image_number, config=CONFIG_NUMBERS
        ).strip()
        
        try:
            if res_number:
                res_number = int(res_number)
        except ValueError as exc:
            raise NotANumberException(res_number) from exc

        res_item = pytesseract.image_to_string(image_item, config=CONFIG_ITEMS).strip()
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

        if score < 20:
            continue

        results[match] = res_number

        if debug_files:
            save_debug_image(image_number, image_item, index)

    return results
