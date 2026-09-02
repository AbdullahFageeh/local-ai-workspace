import hashlib

def hash_sha256(text: str) -> str:
    """
    Compute and return the hex SHA-256 hash of an input string.

    Args:
        text (str): The input string to hash.

    Returns:
        str: The hex SHA-256 hash of the input string.

    Raises:
        TypeError: If the input is not a string.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    sha256_hash = hashlib.sha256(text.encode()).hexdigest()
    return sha256_hash