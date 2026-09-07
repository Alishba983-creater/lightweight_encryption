import hashlib
import hmac
from dataclasses import dataclass

import numpy as np

from .algorithm6 import encrypt_image
from .algorithm9 import parameter_initialization


MASTER_KEY_SIZE = 32


@dataclass
class CipherContext:
    """
    Contains all values derived from the master key.

    These are calculated once and reused for multiple images.
    """

    master_key: bytes
    derived_material: bytes
    himage: list
    r0: float
    r1: float
    r2: float
    initial_x: float


def derive_master_material(master_key: bytes) -> bytes:

    if not isinstance(master_key, bytes):
        raise TypeError("master_key must be bytes")

    if len(master_key) != MASTER_KEY_SIZE:
        raise ValueError(
            "master_key must be exactly 32 bytes."
        )

    return hmac.new(
        master_key,
        b"DataShield-Image-Encryption",
        hashlib.sha256
    ).digest()


def derive_himage(derived_material: bytes) -> list:

    digest = hashlib.sha512(
        derived_material
    ).digest()

    return list(digest)


def derive_initial_x(derived_material: bytes) -> float:

    value = int.from_bytes(
        derived_material[:8],
        byteorder="big"
    )

    x = value / float(2**64 - 1)

    if x <= 0.0:
        x = 1e-12

    if x >= 1.0:
        x = 1.0 - 1e-12

    return x


def initialize_cipher(master_key: bytes) -> CipherContext:
    """
    Perform all master-key-dependent calculations ONCE.

    Call this once when the encryption session starts.
    """

    derived_material = derive_master_material(
        master_key
    )

    himage = derive_himage(
        derived_material
    )

    r0, r1, r2 = parameter_initialization(
        himage
    )

    initial_x = derive_initial_x(
        derived_material
    )

    return CipherContext(
        master_key=master_key,
        derived_material=derived_material,
        himage=himage,
        r0=r0,
        r1=r1,
        r2=r2,
        initial_x=initial_x
    )


def encrypt(
    img: np.ndarray,
    context: CipherContext,
    R: int = 4,
    C: int = 4
):
    """
    Encrypt one image using an already initialized context.

    No master-key material is recalculated here.
    """

    if not isinstance(img, np.ndarray):
        raise TypeError(
            "img must be a NumPy array"
        )

    if img.dtype != np.uint8:
        raise ValueError(
            "Image must have dtype uint8."
        )

    encrypted_image = encrypt_image(
        img=img,
        hkey=context.master_key,
        himage=context.himage,
        R=R,
        C=C,
        r0=context.r0,
        r1=context.r1,
        r2=context.r2,
        x=context.initial_x
    )

    return encrypted_image