from datetime import datetime
from pathlib import Path

import pytesseract
from PIL import Image

from endfield_ocr_core.split_image import split_image
from endfield_ocr_core.preprocess import preprocess


def get_number(img: Image.Image, rows: int, cols: int, region: str, debug_files=False) -> list[str]:
    config = r"--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789"
    
    img_list = split_image(img, rows, cols)
    
    result_list: list[str] = []
    
    for index, image in enumerate(img_list):
        image = preprocess(image, index, region)
        result_list.append(pytesseract.image_to_string(image, config=config).strip())
        
        if debug_files:
            now = datetime.now().strftime("%Y_%m_%d_%H-%M")
            image_name = str(index + 1) + ".png"
            base_dir = Path(__file__).parent / "Debug Images"
            sub_dir = base_dir / now
            
            if not base_dir.exists():
                base_dir.mkdir(parents=True, exist_ok=True)
            
            if not sub_dir.exists():
                sub_dir.mkdir(parents=True, exist_ok=True)
                
            img_path = sub_dir / image_name
            image.save(str(img_path))
        
    return result_list
