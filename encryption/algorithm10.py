import random


# ============================================================
# ALGORITHM 10
# HKEY_SEQUENCE(hkey, start, jump)
# ============================================================

def hkey_sequence(hkey, start, jump):
    """
    Algorithm 10: HKEY_SEQUENCE

    Input:
        hkey  - sequence of keys
        start - starting index
        jump  - increment value

    Output:
        total - sum of selected elements in the sequence
    """

    # Initialize sum as 0
    total = 0

    # For i from start to length of hkey - 1,
    # with step size jump
    for i in range(start, len(hkey), jump):
        total += hkey[i]

    # Return sum
    return total


