import numpy as np

from encryption.algorithm4 import generate_key_sequence
from encryption.algorithm1 import make_image_tiles
from encryption.algorithm7 import random_number
from decryption.algorithm13 import inv_shift_tiles
from encryption.algorithm8 import combine_image_tiles


def decrypt_image(eimg, hkey, himage, R, C, r0, r1, r2, x):
    """
    Decrypt grayscale, RGB, or RGBA uint8 images.

    This function is the exact inverse of algorithm6.py.
    """

    if not isinstance(eimg, np.ndarray):
        raise TypeError("eimg must be a NumPy array")

    if eimg.ndim not in (2, 3):
        raise ValueError(
            "Only grayscale (H,W) or color (H,W,C) images are supported."
        )

    if eimg.dtype != np.uint8:
        raise ValueError("Encrypted image must have dtype uint8.")

    if len(himage) < 64:
        raise ValueError("himage must contain at least 64 values.")

    # ---------------------------------------------------------
    # 1. Divide encrypted image into tiles
    # ---------------------------------------------------------
    tiles, part_height, part_width, fpart_height, fpart_width = (
        make_image_tiles(eimg, R, C)
    )

    # ---------------------------------------------------------
    # 2. Generate exactly the same X sequence
    # ---------------------------------------------------------
    X = generate_key_sequence(
        x,
        r2,
        fpart_height,
        fpart_width
    )

    # Preserve the x value used for shuffling: encryption called
    # shift_tiles(...) with the initial x (before any random_number
    # updates). Save it so we can pass the same x to inv_shift_tiles.
    x_for_shuffle = x

    decrypted_tiles = []

    # ---------------------------------------------------------
    # 3. Decrypt each encrypted tile
    # ---------------------------------------------------------

            # Same IV initialization as encryption
    IV = np.zeros(
    (fpart_height, fpart_width, eimg.shape[2]) if eimg.ndim == 3 else (fpart_height, fpart_width),
    dtype=np.uint8
    )

    for e_tile in tiles:


        decrypted_tile = np.zeros_like(
            e_tile,
            dtype=np.uint8
        )

        trows = e_tile.shape[0]
        tcols = e_tile.shape[1]

        k = 0

        for i in range(trows):
            for j in range(tcols):

                # MUST generate the same rd sequence
                rd, x = random_number(x, r1)

                key_value = int(X[k]) ^ int(himage[rd])

                if e_tile.ndim == 2:
                    # -----------------------------------------
                    # Grayscale
                    # -----------------------------------------
                    ciphertext = int(e_tile[i, j])

                    plaintext = (
                        ciphertext
                        ^ key_value
                        ^ int(IV[i, j])
                    )

                    decrypted_tile[i, j] = plaintext

                    # IMPORTANT:
                    # Encryption updated IV with plaintext.
                    IV[i, j] = IV[i, j] ^ plaintext

                else:
                    # -----------------------------------------
                    # RGB / RGBA
                    # -----------------------------------------
                    channels = e_tile.shape[2]

                    for c in range(channels):

                        ciphertext = int(
                            e_tile[i, j, c]
                        )

                        plaintext = (
                            ciphertext
                            ^ key_value
                            ^ int(IV[i, j, c])
                        )

                        decrypted_tile[i, j, c] = plaintext

                        # Same state update as encryption
                        IV[i, j, c] = IV[i, j, c] ^ plaintext

                k += 1

        decrypted_tiles.append(decrypted_tile)

    # ---------------------------------------------------------
    # 4. Reverse tile shuffling
    # ---------------------------------------------------------
    original_tiles = inv_shift_tiles(
        decrypted_tiles,
        R,
        C,
        x_for_shuffle,
        r=r0
    )

    # ---------------------------------------------------------
    # 5. Reconstruct original image
    # ---------------------------------------------------------
    decrypted_image = combine_image_tiles(
        original_tiles,
        R,
        C
    )

    return decrypted_image