import cv2
import numpy as np
from numpy.typing import NDArray

def detect_edges(region: NDArray) -> NDArray:
    grey = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    if grey.dtype != np.uint8:
        grey = np.clip(grey, 0, 255).astype(np.uint8)
    blurred = cv2.GaussianBlur(grey, (5, 5), 0)
    return cv2.Canny(blurred, 50, 150)