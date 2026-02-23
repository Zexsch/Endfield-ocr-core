from datetime import datetime

from PIL.Image import Image

from endfield_ocr_core.utils.package_dirs import PackageDirs

def save_debug_image(image_number: Image, image_item: Image, index: int) -> None:
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