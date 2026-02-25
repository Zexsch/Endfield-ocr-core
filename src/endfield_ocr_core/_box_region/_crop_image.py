import numpy as np
from PIL import Image

from endfield_ocr_core._box_region._crop_bottom import crop_bottom
from endfield_ocr_core._box_region._crop_top import crop_top
from endfield_ocr_core._box_region._crop_width import crop_width
from endfield_ocr_core.models.bounding_box import BoundingBoxRaw
from endfield_ocr_core.utils.package_dirs import PackageDirs


def crop_image(img: Image.Image, debug_file=False) -> BoundingBoxRaw:
    img_np = np.array(img)
    _, img_h = img_np.shape[:2]

    region_y = crop_top(img_np)

    region = img_np[region_y : img_h - region_y, :]

    cropped_lr, left_trim, final_w = crop_width(region=region)
    _, final_h = crop_bottom(cropped_lr)

    final_x = int(left_trim)
    final_y = int(region_y)
    final_w = int(final_w)
    final_h = int(final_h)

    res = BoundingBoxRaw(final_x, final_y, final_w, final_h)

    if debug_file:
        crop_img = img.crop((final_x, final_y, final_x + final_w, final_y + final_h))
        crop_img.save(PackageDirs().debug_files_dir / "crop_img.png")

    return res
