import numpy as np
from PIL.Image import Image

from endfield_ocr_core.region._crop_bottom import crop_bottom
from endfield_ocr_core.region._crop_top import crop_top
from endfield_ocr_core.region._crop_width import crop_width
from endfield_ocr_core.models.bounding_box import BoundingBoxRaw


def crop_image(img: Image) -> BoundingBoxRaw:
    img_np = np.array(img)

    bbox = crop_top(img_np)
    region = img_np[bbox.y : bbox.y + bbox.height, bbox.x : bbox.x + bbox.width]

    cropped_lr, left_trim, final_w = crop_width(region=region)
    _, final_h = crop_bottom(cropped_lr)

    final_x = int(bbox.x + left_trim)
    final_y = int(bbox.y)
    final_w = int(final_w)
    final_h = int(final_h)

    return BoundingBoxRaw(final_x, final_y, final_w, final_h)
