from encryption.algorithm2 import generate_image_shuffling_pattern


def inv_shift_tiles(
    stiles: list,
    R: int,
    C: int,
    x: float,
    r: float
) -> list:
    """
    Algorithm 13: INV_SHIFT_TILES

    Input:
        stiles : list containing the shifted tiles
        R      : number of rows in the tile grid
        C      : number of columns in the tile grid
        x      : initial value for the shuffling pattern
        r      : constant value for shuffling

    Output:
        temp   : list containing the inverted shifted tiles
    """

    total_elements = R * C

    # Validate number of tiles
    if len(stiles) != total_elements:
        raise ValueError(
            f"Expected {total_elements} tiles, "
            f"but received {len(stiles)}."
        )

    # Generate the SAME shuffling pattern
    index = generate_image_shuffling_pattern(
        x=x,
        r0=r,
        R=R,
        C=C
    )

    # Initialize temp
    temp = [None] * total_elements

    # Algorithm 13:
    #
    # for i = 0 to R*C-1
    #     temp[index[i]] = stiles[i]

    for i in range(total_elements):
        temp[index[i]] = stiles[i]

    return temp