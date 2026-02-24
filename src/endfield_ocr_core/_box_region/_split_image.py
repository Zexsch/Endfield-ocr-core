from PIL.Image import Image

from endfield_ocr_core.utils._get_config import _get_config


def split_image(img: Image, region: str) -> list[Image]:
    img_width, img_height = img.size

    config = _get_config(region)
    rows = config["split"]["rows"]
    cols = config["split"]["cols"]

    cells = []
    for row in range(rows):
        for col in range(cols):
            left = int(col * img_width / cols)
            right = int((col + 1) * img_width / cols)
            top = int(row * img_height / rows)
            bottom = int((row + 1) * img_height / rows)

            cell_img = img.crop((left, top, right, bottom))
            cells.append(cell_img)

    return cells
