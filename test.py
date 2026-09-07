import random

# ============================================================
# ALGORITHM 11: CONVERT_TO_FLOAT(seed)
# ============================================================
def convert_to_float(seed):
    """
    Generates a random float between 3.57 and 4.0 using the seed.
    Uses an independent generator so call order doesn't mess up values.
    """
    # Create an isolated random instance
    rng = random.Random(seed)
    
    # Generate random float between 3.57 and 4.0
    random_float = rng.uniform(3.57, 4.0)
    
    return random_float


# ============================================================
# ALGORITHM 10: HKEY_SEQUENCE(hkey, start, jump)
# ============================================================
def hkey_sequence(hkey, start, jump):
    """
    Sums numbers in hkey starting from index 'start' with a step size of 'jump'.
    """
    total = 0
    for i in range(start, len(hkey), jump):
        total += hkey[i]
    return total


# ============================================================
# ALGORITHM 9: PARAMETER_INITIALIZATION(himage)
# ============================================================
def parameter_initialization(himage):
    """
    Calculates parameter values r0, r1, and r2 using Algorithms 10 and 11.
    """
    # Step 1: Calculate sums using Algorithm 10
    var0 = hkey_sequence(himage, 0, 4)
    var1 = hkey_sequence(himage, 1, 4)
    var2 = hkey_sequence(himage, 1, 1)

    # Step 2: Convert sums to floats using Algorithm 11
    r0 = convert_to_float(var0)
    r1 = convert_to_float(var1)
    r2 = convert_to_float(var2)

    return r0, r1, r2


# ============================================================
# TEST RUN
# ============================================================
if __name__ == "__main__":
    # Sample input list (e.g., image key or bytes)
    sample_himage = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    # Calculate r0, r1, r2
    r0, r1, r2 = parameter_initialization(sample_himage)

    print("--- Calculated Parameters ---")
    print(f"r0: {r0}")
    print(f"r1: {r1}")
    print(f"r2: {r2}")

    
    # Calculate r0, r1, r2
    r0, r1, r2 = parameter_initialization(sample_himage)

    print("--- Calculated Parameters ---")
    print(f"r0: {r0}")
    print(f"r1: {r1}")
    print(f"r2: {r2}")


    # Test if r1 stays the exact same when called directly during decryption
    var1_check = hkey_sequence(sample_himage, 1, 4)
    r1_check = convert_to_float(var1_check)

    if r1 == r1_check:
        print("\nSUCCESS: Encryption and Decryption values match perfectly!")
    else:
        print("\nFAILED: Values still do not match.")