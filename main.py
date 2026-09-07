import cv2
import numpy as np

from encryption.encrypt import (
    initialize_cipher,
    encrypt
)

from decryption.decrypt import decrypt_image_from_path

from master_key.master_key import generate_master_key


def main():

    # =========================================================
    # SETTINGS
    # =========================================================

    input_path = "test_image.jpg"
    encrypted_path = "encrypted_image.png"
    decrypted_path = "decrypted_image.png"

    R = 4
    C = 4

    # =========================================================
    # 1. LOAD IMAGE
    # =========================================================

    original = cv2.imread(
        input_path,
        cv2.IMREAD_UNCHANGED
    )

    if original is None:
        raise FileNotFoundError(
            f"Could not load {input_path}"
        )

    if original.dtype != np.uint8:
        raise ValueError(
            "Image must be an 8-bit image."
        )

    print("Original image loaded.")
    print("Shape:", original.shape)
    print("Type:", "Grayscale" if original.ndim == 2 else "Color")

    # =========================================================
    # 2. GENERATE MASTER KEY
    # =========================================================

    master_key = generate_master_key("image.jpg")

    if len(master_key) != 32:
        raise ValueError(
            "Master key must be exactly 32 bytes."
        )

    print("Master key generated.")
    print("Key length:", len(master_key), "bytes")

    # =========================================================
    # 3. INITIALIZE CIPHER CONTEXT — ONCE
    # =========================================================

    context = initialize_cipher(master_key)

    print("Cipher context initialized.")

    # =========================================================
    # 4. ENCRYPT IMAGE
    # =========================================================

    encrypted_image = encrypt(
        img=original,
        context=context,
        R=R,
        C=C
    )

    print("Image encrypted.")

    # =========================================================
    # 5. SAVE ENCRYPTED IMAGE
    # =========================================================

    success = cv2.imwrite(
        encrypted_path,
        encrypted_image
    )

    if not success:
        raise IOError(
            "Could not save encrypted image."
        )

    print("Encrypted image saved:", encrypted_path)

    # =========================================================
    # 6. DECRYPT IMAGE
    # =========================================================

    decrypted_image = decrypt_image_from_path(
        encrypted_path=encrypted_path,
        master_key=master_key,
        R=R,
        C=C,
        output_path=decrypted_path
    )

    print("Image decrypted.")
    print("Decrypted image saved:", decrypted_path)

    # =========================================================
    # 7. VERIFY
    # =========================================================

    same_shape = (
        original.shape == decrypted_image.shape
    )

    exact_match = np.array_equal(
        original,
        decrypted_image
    )

    print()
    print("=" * 50)
    print("VERIFICATION")
    print("=" * 50)

    print("Same shape :", same_shape)
    print("Exact match:", exact_match)

    if exact_match:
        print()
        print("SUCCESS!")
        print("Original and decrypted images are identical.")
    else:
        print()
        print("FAILED!")
        print("Original and decrypted images are different.")

        difference = np.abs(
            original.astype(np.int16)
            - decrypted_image.astype(np.int16)
        )

        print("Different values:", np.count_nonzero(difference))
        print("Maximum difference:", difference.max())

    print("=" * 50)


if __name__ == "__main__":
    main()