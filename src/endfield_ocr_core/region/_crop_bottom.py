import cv2
import numpy as np


def crop_bottom(
    region,
    edge_threshold_ratio=0.2,
    smooth_kernel=21,
    ignore_bottom_ratio=0.0,
    min_height_fraction=0.05,
):
    """
    Crop only the bottom edge of a region to the last structural content.
    Returns cropped image and height.
    """

    grey = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    if grey.dtype != np.uint8:
        grey = np.clip(grey, 0, 255).astype(np.uint8)

    blurred = cv2.GaussianBlur(grey, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    h, _ = edges.shape

    # Horizontal edges only (rows)
    crop_limit_h = int(h * (1 - ignore_bottom_ratio))
    edges_crop_h = edges[:crop_limit_h, :]
    row_sum = np.sum(edges_crop_h > 0, axis=1).astype(np.float32)
    row_sum_smooth = np.convolve(
        row_sum, np.ones(smooth_kernel) / smooth_kernel, mode="same"
    )
    row_sum_smooth /= np.max(row_sum_smooth) + 1e-6

    row_indices = np.where(row_sum_smooth > edge_threshold_ratio)[0]

    if len(row_indices) == 0:
        bottom = h
    else:
        bottom = row_indices[-1]  # keep top intact, just adjust bottom

    # ignore tiny bottom crops
    if (bottom - 0) < h * min_height_fraction:
        bottom = h

    cropped = region[:bottom, :]
    return cropped, bottom
