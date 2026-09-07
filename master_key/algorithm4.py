def generate_key_stream(x, r2, rows, cols):
    """
    Generate a key stream using Algorithm 4.

    Parameters:
        x    : Initial random value
        r2   : Logistic map parameter
        rows : Number of rows
        cols : Number of columns

    Returns:
        bytes: Generated key stream
    """

    key = bytearray()

    # Total key values required
    total_values = rows * cols

    for _ in range(total_values):

        # Logistic map
        x = r2 * x * (1 - x)

        # Convert chaotic value into a byte (0-255)
        key_value = int(x * 10**12) % 256

        key.append(key_value)

    return bytes(key)