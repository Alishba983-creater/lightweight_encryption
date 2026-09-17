import cv2
import numpy as np
import os
import time
import psutil

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from encryption.encrypt import (
    initialize_cipher,
    encrypt
)

from decryption.decrypt import decrypt_image_from_path

from master_key.master_key import generate_master_key


# =========================================================
# SETTINGS
# =========================================================

INPUT_PATH = "test_image.jpg"

LIGHTWEIGHT_ENCRYPTED_PATH = "encrypted_lightweight.png"
LIGHTWEIGHT_DECRYPTED_PATH = "decrypted_lightweight.png"

AES_ENCRYPTED_PATH = "encrypted_aes.bin"
AES_DECRYPTED_PATH = "decrypted_aes.png"

R = 4
C = 4

NUMBER_OF_RUNS = 5


# =========================================================
# AES-256-GCM ENCRYPTION
# =========================================================

def aes_encrypt(image, key, output_path):
    """
    Encrypt image using AES-256-GCM.
    """

    # Convert image to raw bytes
    image_bytes = image.tobytes()

    # Store shape and dtype information
    shape = np.array(image.shape, dtype=np.int32)

    shape_bytes = shape.tobytes()

    # AES-GCM requires a 12-byte nonce
    nonce = os.urandom(12)

    aesgcm = AESGCM(key)

    start_time = time.perf_counter()

    encrypted_data = aesgcm.encrypt(
        nonce,
        image_bytes,
        shape_bytes
    )

    end_time = time.perf_counter()

    encryption_time = end_time - start_time

    # -----------------------------------------------------
    # Save nonce + shape + encrypted data
    # -----------------------------------------------------

    with open(output_path, "wb") as f:

        # Save number of dimensions
        f.write(len(image.shape).to_bytes(1, "little"))

        # Save shape
        f.write(shape_bytes)

        # Save nonce
        f.write(nonce)

        # Save encrypted data
        f.write(encrypted_data)

    return encryption_time


# =========================================================
# AES-256-GCM DECRYPTION
# =========================================================

def aes_decrypt(key, input_path, output_path):
    """
    Decrypt AES-256-GCM encrypted image.
    """

    with open(input_path, "rb") as f:

        # Read number of dimensions
        ndim = int.from_bytes(
            f.read(1),
            "little"
        )

        # Read shape
        shape_bytes = f.read(
            ndim * 4
        )

        shape = tuple(
            np.frombuffer(
                shape_bytes,
                dtype=np.int32
            )
        )

        # Read nonce
        nonce = f.read(12)

        # Read encrypted image
        encrypted_data = f.read()

    aesgcm = AESGCM(key)

    start_time = time.perf_counter()

    decrypted_data = aesgcm.decrypt(
        nonce,
        encrypted_data,
        shape_bytes
    )

    end_time = time.perf_counter()

    decryption_time = end_time - start_time

    # Convert bytes back to image
    decrypted_image = np.frombuffer(
        decrypted_data,
        dtype=np.uint8
    ).reshape(shape)

    # Save image
    cv2.imwrite(
        output_path,
        decrypted_image
    )

    return decrypted_image, decryption_time


# =========================================================
# MEMORY MEASUREMENT
# =========================================================

def get_memory_usage():
    """
    Returns current process memory usage in MB.
    """

    process = psutil.Process(
        os.getpid()
    )

    memory_bytes = process.memory_info().rss

    memory_mb = memory_bytes / (
        1024 * 1024
    )

    return memory_mb


# =========================================================
# LIGHTWEIGHT ENCRYPTION TEST
# =========================================================

def test_lightweight(original, master_key):

    print("\n")
    print("=" * 60)
    print("LIGHTWEIGHT ENCRYPTION")
    print("=" * 60)

    context = initialize_cipher(
        master_key
    )

    encryption_times = []
    decryption_times = []
    memory_values = []

    # -----------------------------------------------------
    # Encryption
    # -----------------------------------------------------

    for i in range(NUMBER_OF_RUNS):

        start_memory = get_memory_usage()

        start_time = time.perf_counter()

        encrypted_image = encrypt(
            img=original,
            context=context,
            R=R,
            C=C
        )

        end_time = time.perf_counter()

        end_memory = get_memory_usage()

        encryption_time = (
            end_time - start_time
        )

        memory_used = (
            end_memory - start_memory
        )

        encryption_times.append(
            encryption_time
        )

        memory_values.append(
            memory_used
        )

    # Save final encrypted image
    cv2.imwrite(
        LIGHTWEIGHT_ENCRYPTED_PATH,
        encrypted_image
    )

    # -----------------------------------------------------
    # Decryption
    # -----------------------------------------------------

    for i in range(NUMBER_OF_RUNS):

        start_time = time.perf_counter()

        decrypted_image = decrypt_image_from_path(
            encrypted_path=LIGHTWEIGHT_ENCRYPTED_PATH,
            master_key=master_key,
            R=R,
            C=C,
            output_path=LIGHTWEIGHT_DECRYPTED_PATH
        )

        end_time = time.perf_counter()

        decryption_time = (
            end_time - start_time
        )

        decryption_times.append(
            decryption_time
        )

    # -----------------------------------------------------
    # Results
    # -----------------------------------------------------

    avg_encryption = np.mean(
        encryption_times
    )

    avg_decryption = np.mean(
        decryption_times
    )

    total_time = (
        avg_encryption +
        avg_decryption
    )

    print(
        f"Average Encryption Time : "
        f"{avg_encryption:.6f} seconds"
    )

    print(
        f"Average Decryption Time : "
        f"{avg_decryption:.6f} seconds"
    )

    print(
        f"Total Time              : "
        f"{total_time:.6f} seconds"
    )

    print(
        f"Average Memory Usage    : "
        f"{np.mean(memory_values):.2f} MB"
    )

    # Verify
    exact_match = np.array_equal(
        original,
        decrypted_image
    )

    print(
        "Decryption Correct      :",
        exact_match
    )

    return {
        "encryption_time": avg_encryption,
        "decryption_time": avg_decryption,
        "total_time": total_time,
        "memory": np.mean(memory_values),
        "correct": exact_match
    }


# =========================================================
# AES TEST
# =========================================================

def test_aes(original, aes_key):

    print("\n")
    print("=" * 60)
    print("AES-256-GCM ENCRYPTION")
    print("=" * 60)

    encryption_times = []
    decryption_times = []
    memory_values = []

    # -----------------------------------------------------
    # AES Encryption
    # -----------------------------------------------------

    for i in range(NUMBER_OF_RUNS):

        start_memory = get_memory_usage()

        encryption_time = aes_encrypt(
            original,
            aes_key,
            AES_ENCRYPTED_PATH
        )

        end_memory = get_memory_usage()

        memory_used = (
            end_memory - start_memory
        )

        encryption_times.append(
            encryption_time
        )

        memory_values.append(
            memory_used
        )

    # -----------------------------------------------------
    # AES Decryption
    # -----------------------------------------------------

    for i in range(NUMBER_OF_RUNS):

        decrypted_image, decryption_time = aes_decrypt(
            aes_key,
            AES_ENCRYPTED_PATH,
            AES_DECRYPTED_PATH
        )

        decryption_times.append(
            decryption_time
        )

    # -----------------------------------------------------
    # Results
    # -----------------------------------------------------

    avg_encryption = np.mean(
        encryption_times
    )

    avg_decryption = np.mean(
        decryption_times
    )

    total_time = (
        avg_encryption +
        avg_decryption
    )

    print(
        f"Average Encryption Time : "
        f"{avg_encryption:.6f} seconds"
    )

    print(
        f"Average Decryption Time : "
        f"{avg_decryption:.6f} seconds"
    )

    print(
        f"Total Time              : "
        f"{total_time:.6f} seconds"
    )

    print(
        f"Average Memory Usage    : "
        f"{np.mean(memory_values):.2f} MB"
    )

    # Verify
    exact_match = np.array_equal(
        original,
        decrypted_image
    )

    print(
        "Decryption Correct      :",
        exact_match
    )

    return {
        "encryption_time": avg_encryption,
        "decryption_time": avg_decryption,
        "total_time": total_time,
        "memory": np.mean(memory_values),
        "correct": exact_match
    }


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 60)
    print("LIGHTWEIGHT ENCRYPTION vs AES-256-GCM")
    print("=" * 60)

    # -----------------------------------------------------
    # Load image
    # -----------------------------------------------------

    original = cv2.imread(
        INPUT_PATH,
        cv2.IMREAD_UNCHANGED
    )

    if original is None:
        raise FileNotFoundError(
            f"Could not load {INPUT_PATH}"
        )

    if original.dtype != np.uint8:
        raise ValueError(
            "Image must be an 8-bit image."
        )

    print("\nImage Information")
    print("-" * 60)

    print("Image path :", INPUT_PATH)
    print("Shape      :", original.shape)
    print("Data type  :", original.dtype)

    image_size_bytes = original.nbytes

    image_size_mb = (
        image_size_bytes /
        (1024 * 1024)
    )

    print(
        f"Image size : {image_size_mb:.4f} MB"
    )

    # -----------------------------------------------------
    # Generate 32-byte master key
    # -----------------------------------------------------

    master_key = generate_master_key(
        "image.jpg"
    )

    if len(master_key) != 32:
        raise ValueError(
            "Master key must be exactly 32 bytes."
        )

    print(
        "\nMaster key length:",
        len(master_key),
        "bytes"
    )

    # -----------------------------------------------------
    # AES requires 32-byte key for AES-256
    # -----------------------------------------------------

    aes_key = master_key

    # -----------------------------------------------------
    # Lightweight scheme
    # -----------------------------------------------------

    lightweight_results = test_lightweight(
        original,
        master_key
    )

    # -----------------------------------------------------
    # AES
    # -----------------------------------------------------

    aes_results = test_aes(
        original,
        aes_key
    )

    # -----------------------------------------------------
    # Throughput
    # -----------------------------------------------------

    lightweight_encryption_throughput = (
        image_size_mb /
        lightweight_results["encryption_time"]
    )

    aes_encryption_throughput = (
        image_size_mb /
        aes_results["encryption_time"]
    )

    lightweight_decryption_throughput = (
        image_size_mb /
        lightweight_results["decryption_time"]
    )

    aes_decryption_throughput = (
        image_size_mb /
        aes_results["decryption_time"]
    )

    # -----------------------------------------------------
    # Final comparison
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("FINAL PERFORMANCE COMPARISON")
    print("=" * 70)

    print(
        f"{'Metric':<30}"
        f"{'Lightweight':<20}"
        f"{'AES-256-GCM':<20}"
    )

    print("-" * 70)

    print(
        f"{'Encryption Time (s)':<30}"
        f"{lightweight_results['encryption_time']:<20.6f}"
        f"{aes_results['encryption_time']:<20.6f}"
    )

    print(
        f"{'Decryption Time (s)':<30}"
        f"{lightweight_results['decryption_time']:<20.6f}"
        f"{aes_results['decryption_time']:<20.6f}"
    )

    print(
        f"{'Total Time (s)':<30}"
        f"{lightweight_results['total_time']:<20.6f}"
        f"{aes_results['total_time']:<20.6f}"
    )

    print(
        f"{'Memory Usage (MB)':<30}"
        f"{lightweight_results['memory']:<20.2f}"
        f"{aes_results['memory']:<20.2f}"
    )

    print(
        f"{'Encryption Throughput MB/s':<30}"
        f"{lightweight_encryption_throughput:<20.4f}"
        f"{aes_encryption_throughput:<20.4f}"
    )

    print(
        f"{'Decryption Throughput MB/s':<30}"
        f"{lightweight_decryption_throughput:<20.4f}"
        f"{aes_decryption_throughput:<20.4f}"
    )

    print(
        f"{'Correct Decryption':<30}"
        f"{str(lightweight_results['correct']):<20}"
        f"{str(aes_results['correct']):<20}"
    )

    print("=" * 70)


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()