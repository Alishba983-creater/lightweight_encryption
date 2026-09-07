import cv2
import numpy as np

from encryption.encrypt import (
    derive_master_material,
    derive_himage,
    derive_initial_x
)

from encryption.algorithm9 import parameter_initialization
from decryption.algorithm12 import decrypt_image


def decrypt_image_from_path(
    encrypted_path,
    master_key,
    R,
    C,
    output_path
):
    """
    Load encrypted PNG, derive all parameters from the master key,
    decrypt, and optionally save the result.
    """
   
    if not isinstance(master_key, bytes):
        raise TypeError(
            "master_key must be bytes."
        )

    if len(master_key) != 32:
        raise ValueError(
            "master_key must be exactly 32 bytes."
        )

    # ---------------------------------------------------------
    # 1. Load encrypted image without changing channels
    # ---------------------------------------------------------
    encrypted_image = cv2.imread(
        encrypted_path,
        cv2.IMREAD_UNCHANGED
    )

    if encrypted_image is None:
        raise FileNotFoundError(
            f"Could not load: {encrypted_path}"
        )

    if encrypted_image.dtype != np.uint8:
        raise ValueError(
            "Encrypted image must be uint8."
        )

    # ---------------------------------------------------------
    # 2. Derive same material from master key
    # ---------------------------------------------------------
    derived_material = derive_master_material(
        master_key
    )

    # ---------------------------------------------------------
    # 3. Derive HIMAGE
    # ---------------------------------------------------------
    himage = derive_himage(
        derived_material
    )

    # ---------------------------------------------------------
    # 4. Derive r0, r1, r2
    # ---------------------------------------------------------
    r0, r1, r2 = parameter_initialization(
        himage
    )

    # ---------------------------------------------------------
    # 5. Derive same initial x
    # ---------------------------------------------------------
    x = derive_initial_x(
        derived_material
    )

    # ---------------------------------------------------------
    # 6. Decrypt
    # ---------------------------------------------------------
    decrypted_image = decrypt_image(
        eimg=encrypted_image,
        hkey=master_key,
        himage=himage,
        R=R,
        C=C,
        r0=r0,
        r1=r1,
        r2=r2,
        x=x
    )
    
    # ---------------------------------------------------------
    # 7. Optionally save
    # ---------------------------------------------------------
    if output_path is not None:

        success = cv2.imwrite(
            output_path,
            decrypted_image
        )

        if not success:
            raise IOError(
                f"Could not save: {output_path}"
            )

    return decrypted_image