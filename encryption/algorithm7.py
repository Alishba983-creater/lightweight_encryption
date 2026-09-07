import math


def random_number(x: float, r1: float):
    """
    Algorithm 7: RandomNumber(x, r1)

    Generates a chaotic random index in the range 0 to 63.

    Returns:
        rnd: Randomly generated index
        x: Updated chaotic value
    """

    # Chaotic logistic map
    x = r1 * x * (1 - x)

    # Generate index from 0 to 63
    rnd = math.floor(
        x * math.floor(
            x * math.pow(7, 13) - 1
        )
    ) % 64

    return rnd, x