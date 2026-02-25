import cv2
import pytesseract
import numpy as np
from PIL import Image

from endfield_ocr_core.models.exceptions import MarketBBoxNotFound
from endfield_ocr_core.config.config import CONFIG_CROP_TOP
from endfield_ocr_core.utils.package_dirs import PackageDirs


def crop_top(
    image: np.typing.NDArray, padding_y: int = 10, second_run=False, orig_crop_height=0
) -> float:
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grey = cv2.GaussianBlur(grey, (3, 3), 0)

    data = pytesseract.image_to_data(
        grey, output_type=pytesseract.Output.DICT, config=CONFIG_CROP_TOP
    )

    n_boxes = len(data["text"])

    market_box = None

    for i in range(n_boxes):
        word = data["text"][i].strip().lower()

        if word == "market." and not second_run:
            # catch upper "Check them out at the market." area
            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            region_y = y + h + padding_y

            image = image[region_y:, :]

            img = Image.fromarray(image)
            img.save(PackageDirs().debug_files / "debug2.png")

            img = np.array(img)
            return crop_top(img, second_run=True, orig_crop_height=region_y)

        if word == "market":
            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]
            market_box = (x, y, w, h)
            break

    if market_box is None:
        raise MarketBBoxNotFound()

    x, y, w, h = market_box

    region_y = y + h + padding_y

    image = image[region_y:, :]

    img = Image.fromarray(image)
    img.save(PackageDirs().debug_files / "debug_crop_last.png")

    return region_y + orig_crop_height
