import hashlib
import numpy as np


# ============================================================
# ALGORITHM 5
# CONVERT_HASH_TO_INTEGER_LIST
# ============================================================

def convert_hash_to_integer_list(
    img: np.ndarray,
    str1: str = ""
) -> list:
    """
    Algorithm 5: CONVERT_HASH_TO_INTEGER_LIST

    Creates a SHA3-512 hash from the actual image bytes
    and an optional additional string.

    Supports:
        Grayscale: (H, W)
        RGB:       (H, W, 3)
        RGBA:      (H, W, 4)

    Output:
        hkey: List containing 64 integers in range 0-255.
    """

    if not isinstance(img, np.ndarray):
        raise TypeError("img must be a NumPy array.")

    # Use the actual binary image data.
    # This preserves all channels for RGB/RGBA images.
    image_bytes = img.tobytes()

    # Additional string converted to bytes.
    extra_bytes = str1.encode("utf-8")

    # Combine image bytes and optional string.
    data = image_bytes + extra_bytes

    # SHA3-512 = 512 bits = 64 bytes.
    hash_digest = hashlib.sha3_512(data).digest()

    # Convert each byte to an integer 0-255.
    hkey = list(hash_digest)

    return hkey