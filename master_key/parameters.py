
import secrets


def generate_initial_parameters():
    """
    Generate cryptographically secure initial parameters
    for Algorithm 4.

    Returns:
        x: Random float where 0 < x < 1
        r2: Random float in the logistic chaotic range
    """

    # Generate x between 0 and 1
    x = secrets.randbelow(10**12) / 10**12

    # Avoid exactly 0
    if x == 0:
        x = 1 / 10**12

    # Generate r2 between 3.6 and 4.0
    r2 = 3.6 + (secrets.randbelow(10**12) / 10**12) * 0.4

    return x, r2