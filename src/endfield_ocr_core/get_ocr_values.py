from datetime import datetime

import pytesseract
from PIL import Image
from rapidfuzz import process, fuzz

from endfield_ocr_core.utils.split_image import split_image
from endfield_ocr_core.utils.preprocess import preprocess
from endfield_ocr_core.models.exceptions import ItemNotFoundException
from endfield_ocr_core.utils.package_dirs import PackageDirs
from endfield_ocr_core.models.config import (
    CropTypes,
    Region,
    WULING_ITEM_NAMES,
    VALLEY_ITEM_NAMES,
)


def get_ocr_values(
    img: Image.Image, rows: int, cols: int, region: str, debug_files=False
) -> dict[str, str]:
    config_numbers = r"--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789"
    config_items = r"--oem 3 --psm 6 -c preserve_interword_spaces=1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789[]'-"

    img_list = split_image(img, rows, cols)

    results: dict[str, str] = {}

    for index, image in enumerate(img_list):
        if region == Region.VALLEY.value and index >= 13:
            continue

        image_number = preprocess(image, index, region, CropTypes.NUMBER)
        image_item = preprocess(image, index, region, CropTypes.ITEM)
        res_number = pytesseract.image_to_string(
            image_number, config=config_numbers
        ).strip()

        res_item = pytesseract.image_to_string(image_item, config=config_items).strip()
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
            now = datetime.now().strftime("%Y_%m_%d_%H-%M")
            image_name_number = str(f"{index+1}_NUMBER") + ".png"
            image_name_item = str(f"{index+1}_ITEM") + ".png"
            base_dir = PackageDirs().debug_files_dir / "Debug Images"
            sub_dir = base_dir / now

            if not sub_dir.exists():
                sub_dir.mkdir(parents=True, exist_ok=True)

            img_path_number = sub_dir / image_name_number
            img_path_item = sub_dir / image_name_item
            image_number.save(str(img_path_number))
            image_item.save(str(img_path_item))

    return results
