from encryption.algorithm3 import shift_tiles
from decryption.algorithm13 import inv_shift_tiles


def run_test(R=3, C=3, x=0.42, r=3.89):
    # Create simple tiles as integers for easy comparison
    original_tiles = [f"Tile_{i}" for i in range(R * C)]

    print("Original:", original_tiles)

    shuffled = shift_tiles(original_tiles, R, C, x, r)
    print("Shuffled:", shuffled)

    restored = inv_shift_tiles(shuffled, R, C, x, r)
    print("Restored:", restored)

    if original_tiles == restored:
        print("RESULT: OK — restored matches original")
        return 0
    else:
        print("RESULT: FAIL — restored DOES NOT match original")
        # Show mismatches
        for i, (a, b) in enumerate(zip(original_tiles, restored)):
            if a != b:
                print(f"Mismatch at index {i}: original={a} restored={b}")
        return 1


if __name__ == '__main__':
    import sys
    exit_code = run_test()
    sys.exit(exit_code)
