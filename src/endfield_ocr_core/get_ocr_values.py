import pytesseract
from PIL import Image

from endfield_ocr_core.region.split_image import split_image
from endfield_ocr_core.utils.preprocess import preprocess
from endfield_ocr_core.utils.debug_image_save import save_debug_image
from endfield_ocr_core.utils.clean_item_name import clean_item_name
from endfield_ocr_core.models.exceptions import NotANumberException
from endfield_ocr_core.config.config import (
    CropTypes,
    Region,
    CONFIG_NUMBERS,
    CONFIG_ITEMS,
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

        match, score = clean_item_name(res_item, region)

        if score < 20:
            continue

        results[match] = res_number

        if debug_files:
            save_debug_image(image_number, image_item, index)

    return results
