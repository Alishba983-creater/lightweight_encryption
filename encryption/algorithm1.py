import math
import numpy as np


def make_image_tiles(image: np.ndarray, R: int, C: int):
    """
    Tiles an input image into R rows and C columns, with edge tiles absorbing
    any remaining pixel remainder from division.
    """
    num_rows = R
    num_cols = C

    # Get dimensions of input image (height, width)
    height, width = image.shape[:2]

    # Calculate base height and width of each part
    part_height = math.floor(height / num_rows)
    part_width = math.floor(width / num_cols)

    # Calculate height and width of the final edge parts
    fpart_height = part_height + (height % num_rows)
    fpart_width = part_width + (width % num_cols)

    image_parts = []

    for r in range(num_rows):
        for c in range(num_cols):
            # Check edge conditions
            is_last_row = r + 1 == num_rows
            is_last_col = c + 1 == num_cols

            if is_last_row and is_last_col:
                y_start = r * part_height
                y_end = (r + 1) * part_height + (height % num_rows)
                x_start = c * part_width
                x_end = (c + 1) * part_width + (width % num_cols)

            elif is_last_row:
                y_start = r * part_height
                y_end = (r + 1) * part_height + (height % num_rows)
                x_start = c * part_width
                x_end = (c + 1) * part_width

            elif is_last_col:
                y_start = r * part_height
                y_end = (r + 1) * part_height
                x_start = c * part_width
                x_end = (c + 1) * part_width + (width % num_cols)

            else:
                y_start = r * part_height
                y_end = (r + 1) * part_height
                x_start = c * part_width
                x_end = (c + 1) * part_width

            # Crop tile
            part = image[y_start:y_end, x_start:x_end]
            image_parts.append(part)

    return image_parts, part_height, part_width, fpart_height, fpart_width