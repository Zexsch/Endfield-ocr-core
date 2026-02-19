from PIL import Image

def split_image(img: Image.Image, rows: int, cols: int) -> list[Image.Image]:
    img_width, img_height = img.size
    
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