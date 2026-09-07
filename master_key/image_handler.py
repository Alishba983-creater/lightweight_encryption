from PIL import Image


def get_image_dimensions(image_path):
    """
    Opens an image and returns its dimensions.

    Returns:
        rows: Image height
        cols: Image width
    """

    with Image.open(image_path) as image:
        cols, rows = image.size

    return rows, cols