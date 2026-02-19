import numpy as np
import cv2
from PIL import Image

from endfield_ocr_core.regions import valley, wuling
from endfield_ocr_core.models.region_not_found import RegionNotFoundException


def get_mult(region: str, index: int) -> dict[str, float]:
    if region == "valley":
        return valley(index)
    if region == "wuling":
        return wuling(index)

    raise RegionNotFoundException(region)


def preprocess(img: Image.Image, index: int, region: str):
    multipliers = get_mult(region, index)
    h_mult = multipliers["h_mult"]
    h_mult_2 = multipliers["h_mult_2"]
    w_mult = multipliers["w_mult"]

    img = img.convert("L")
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    h, w = cv_img.shape[:2]
    cropped = cv_img[int(h * h_mult) : int(h * h_mult_2), int(w * w_mult) :]
    grey = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    grey = cv2.convertScaleAbs(grey, alpha=1.5, beta=0)
    blur = cv2.medianBlur(grey, 3)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    if contours:
        x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
        pad = 8
        cropped = grey[max(0, y - pad) : y + h + pad, max(0, x - pad) : x + w + pad]
    else:
        cropped = grey

    scaled = cv2.resize(thresh, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    _, final = cv2.threshold(scaled, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    pil_image = Image.fromarray(cv2.cvtColor(final, cv2.COLOR_BGR2RGB))

    return pil_image
