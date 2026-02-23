import cv2
import pytesseract
import numpy as np

from endfield_ocr_core.models.bounding_box import BoundingBox
from endfield_ocr_core.models.exceptions import MarketBBoxNotFound


def crop_top(
    image: np.typing.NDArray, padding_y: int = 10, min_confidence: int = 50
) -> BoundingBox:
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grey = cv2.GaussianBlur(grey, (3, 3), 0)

    data = pytesseract.image_to_data(
        grey, output_type=pytesseract.Output.DICT, config="--psm 6"
    )

    n_boxes = len(data["text"])

    market_box = None

    for i in range(n_boxes):
        word = data["text"][i].strip().lower()
        conf = int(data["conf"][i])

        if word == "market" and conf >= min_confidence:
            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]
            market_box = (x, y, w, h)
            break

    if market_box is None:
        raise MarketBBoxNotFound()

    x, y, w, h = market_box

    img_h, img_w = grey.shape

    region_y = y + h + padding_y

    bbox = BoundingBox(0, region_y, img_w, img_h - region_y)

    return bbox
