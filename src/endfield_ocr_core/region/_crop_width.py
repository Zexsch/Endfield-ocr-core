import cv2
import numpy as np


def crop_width(
    region,
    edge_threshold_ratio=0.2,
    smooth_kernel=21,
    ignore_right_ratio=0.08,
    min_width_fraction=0.05,
):
    grey = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    if grey.dtype != np.uint8:
        grey = np.clip(grey, 0, 255).astype(np.uint8)
    blurred = cv2.GaussianBlur(grey, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # ignore extreme right portion
    crop_limit = int(edges.shape[1] * (1 - ignore_right_ratio))
    edges_crop = edges[:, :crop_limit]

    col_sum = np.sum(edges_crop > 0, axis=0).astype(np.float32)
    col_sum_smooth = np.convolve(
        col_sum, np.ones(smooth_kernel) / smooth_kernel, mode="same"
    )
    col_sum_smooth /= np.max(col_sum_smooth) + 1e-6

    indices = np.where(col_sum_smooth > edge_threshold_ratio)[0]

    if len(indices) == 0:
        # fallback: full region
        return region, 0, region.shape[1]

    left = indices[0]
    right = indices[-1]

    # ignore narrow spans (like scrollbars)
    if (right - left) < region.shape[1] * min_width_fraction:
        return region, 0, region.shape[1]

    cropped = region[:, left:right]
    return cropped, left, right - left
