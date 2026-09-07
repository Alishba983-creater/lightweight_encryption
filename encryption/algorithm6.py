import numpy as np

from .algorithm1 import make_image_tiles
from .algorithm3 import shift_tiles
from .algorithm4 import generate_key_sequence
from .algorithm7 import random_number
from .algorithm8 import combine_image_tiles


def encrypt_image(img, hkey, himage, R, C, r0, r1, r2, x):

    # =========================================================
    # 1. DIVIDE IMAGE INTO TILES
    # =========================================================



    tiles, part_height, part_width, fpart_height, fpart_width = (
        make_image_tiles(img, R, C)
    )



    # =========================================================
    # 2. GENERATE KEY SEQUENCE
    # =========================================================

   

    X = generate_key_sequence(
        x,
        r2,
        fpart_height,
        fpart_width
    )

    # =========================================================
    # 3. SHUFFLE TILES
    # =========================================================

   

    stiles = shift_tiles(
        tiles,
        R,
        C,
        x,
        r0
    )


    # =========================================================
    # 4. INITIALIZE IV
    # =========================================================

   

    IV = np.zeros(
        (fpart_height, fpart_width, img.shape[2]) if img.ndim == 3 else (fpart_height, fpart_width),
        dtype=np.uint8
    )


    # =========================================================
    # 5. ENCRYPT TILES
    # =========================================================


    encrypted_tiles = []

    for tile_number, stile in enumerate(stiles):

        # -----------------------------------------------------
        # CREATE ENCRYPTED TILE
        # -----------------------------------------------------

        encrypted_tile = np.zeros_like(
            stile,
            dtype=np.uint8
        )

        trows = stile.shape[0]
        tcols = stile.shape[1]

        k = 0

        # -----------------------------------------------------
        # PIXEL LOOP
        # -----------------------------------------------------

        for i in range(trows):

            for j in range(tcols):

                # =====================================================
                # RANDOM NUMBER
                # =====================================================

                rd, x = random_number(
                    x,
                    r1
                )

                # =====================================================
                # KEY VALUE
                # =====================================================

                key_value = (
                    int(X[k])
                    ^ int(himage[rd])
                )

                # =====================================================
                # GRAYSCALE
                # =====================================================

                if stile.ndim == 2:

                 
                    plaintext = int(
                        stile[i, j]
                    )

                    ciphertext = (
                        plaintext
                        ^ key_value
                        ^ int(IV[i, j])
                    )

                    encrypted_tile[i, j] = ciphertext

                    IV[i, j] = (
                        IV[i, j]
                        ^ plaintext
                    )

                # =====================================================
                # RGB / RGBA
                # =====================================================

                else:

                    channels = stile.shape[2]

                    for c in range(channels):

                        plaintext = int(
                            stile[i, j, c]
                        )

                        ciphertext = (
                            plaintext
                            ^ key_value
                            ^ int(
                                IV[i, j, c]
                            )
                        )

                        encrypted_tile[
                            i, j, c
                        ] = ciphertext

                        IV[
                            i, j, c
                        ] = (
                            IV[i, j, c]
                            ^ plaintext
                        )

                k += 1

        encrypted_tiles.append(
            encrypted_tile
        )

    # =========================================================
    # 6. COMBINE TILES
    # =========================================================

    encrypted_image = combine_image_tiles(
        encrypted_tiles,
        R,
        C
    )


    return encrypted_image