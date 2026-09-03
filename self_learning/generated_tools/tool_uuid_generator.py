import uuid

def generate_uuid() -> str:
    """
    Generates a unique UUID4 string.

    Returns:
        str: A unique UUID4 string.
    """
    return str(uuid.uuid4())