import numpy as np


# ============================================================
# ALGORITHM 8
# COMBINE_IMAGE_TILES(tiles, rows, cols)
# ============================================================

def combine_image_tiles(
    tiles: list,
    rows: int,
    cols: int
) -> np.ndarray:
    """
    Algorithm 8: COMBINE_IMAGE_TILES

    Input:
        tiles - list containing the image tiles
        rows  - number of tile rows
        cols  - number of tile columns

    Output:
        reconstructed_im - reconstructed image
    """

    # Initialize reconstructed image as None
    reconstructed_im = None

    # --------------------------------------------------------
    # Iterate through rows
    # --------------------------------------------------------

    for i in range(rows):

        # Initialize row image as None
        row_im = None

        # ----------------------------------------------------
        # Iterate through columns
        # ----------------------------------------------------

        for j in range(cols):

            # Calculate tile index
            tile_index = i * cols + j

            # Check if tile index is within range
            if tile_index < len(tiles):

                # Get current tile
                tile = tiles[tile_index]

                # Update row image
                if row_im is None:

                    row_im = tile

                else:

                    # Concatenate horizontally
                    row_im = np.concatenate(
                        (row_im, tile),
                        axis=1
                    )

        # ----------------------------------------------------
        # Update reconstructed image
        # ----------------------------------------------------

        if row_im is not None:

            if reconstructed_im is None:

                reconstructed_im = row_im

            else:

                # Concatenate vertically
                reconstructed_im = np.concatenate(
                    (reconstructed_im, row_im),
                    axis=0
                )

    # Return reconstructed image
    return reconstructed_im