from PIL import Image
import secrets
import hashlib

from master_key.algorithm4 import generate_key_stream
from master_key.image_handler import get_image_dimensions
from master_key.parameters import generate_initial_parameters


# ==========================================
# CONFIGURATION
# ==========================================

MASTER_KEY_SIZE = 32  # 256-bit Master Key


# ==========================================
# DERIVE 256-BIT MASTER KEY
# ==========================================

def derive_master_key(key_stream):
    """
    Convert the generated key stream into
    a fixed 256-bit Master Key using SHA-256.
    """

    return hashlib.sha256(key_stream).digest()


# ==========================================
# MAIN FUNCTION
# ==========================================

def generate_master_key(image_path):
    """
    MAIN FUNCTION

    This is the function your Node.js server
    can ultimately call.

    Process:

    Image
      ↓
    Get rows + columns
      ↓
    Generate random x + r2
      ↓
    Algorithm 4
      ↓
    Key Stream
      ↓
    SHA-256
      ↓
    256-bit Master Key

    Returns:
        bytes: 32-byte Master Key
    """

    # Step 1: Get image dimensions
    rows, cols = get_image_dimensions(image_path)

    # Step 2: Generate secure random parameters
    x, r2 = generate_initial_parameters()

    # Step 3: Generate key stream
    key_stream = generate_key_stream(
        x,
        r2,
        rows,
        cols
    )

    # Step 4: Generate 256-bit Master Key
    master_key = derive_master_key(key_stream)

    return master_key