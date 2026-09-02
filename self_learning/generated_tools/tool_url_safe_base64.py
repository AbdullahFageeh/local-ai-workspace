import base64

def encode_url_safe_b64(data: str) -> str:
    """
    Encodes the given string data into a URL-safe Base64 string without padding.

    Args:
        data (str): The string data to be encoded.

    Returns:
        str: The URL-safe Base64 encoded string.

    Raises:
        TypeError: If the input data is not a string.
    """
    if not isinstance(data, str):
        raise TypeError("Input data must be a string")

    # Encode the string to bytes
    data_bytes = data.encode('utf-8')

    # Perform Base64 encoding
    base64_bytes = base64.urlsafe_b64encode(data_bytes)

    # Remove padding
    base64_str = base64_bytes.rstrip(b'=').decode('utf-8')

    return base64_str