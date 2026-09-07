from encryption.algorithm10 import hkey_sequence
from encryption.algorithm11 import convert_to_float


def parameter_initialization(himage):

    """
    Algorithm 9: PARAMETER_INITIALIZATION

    Input:
        himage - integer list / sequence

    Output:
        r0, r1, r2
    """

    # Algorithm 10
    var0 = hkey_sequence(himage, 0, 4)

    # Algorithm 10
    var1 = hkey_sequence(himage, 1, 4)

    # Algorithm 10
    var2 = hkey_sequence(himage, 1, 1)

    # Algorithm 11
    r0 = convert_to_float(var0)

    # Algorithm 11
    r1 = convert_to_float(var1)

    # Algorithm 11
    r2 = convert_to_float(var2)

    return r0, r1, r2