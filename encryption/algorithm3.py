from encryption.algorithm2 import generate_image_shuffling_pattern


def shift_tiles(tiles: list, R: int, C: int, x: float, r: float) -> list:
    """
    Shifts/rearranges image tiles according to the index sequence generated
    by GENERATE_IMAGE_SHUFFLING_PATTERN.
    """
    total_elements = R * C

    # Initialize stiles list of length R * C with None values
    stiles = [None] * total_elements

    # Generate the shuffled index pattern (calls Algorithm 2)
    index = generate_image_shuffling_pattern(x, r, R, C)

    # Rearrange tiles according to generated index array
    for i in range(total_elements):
        stiles[i] = tiles[index[i]]

    return stiles