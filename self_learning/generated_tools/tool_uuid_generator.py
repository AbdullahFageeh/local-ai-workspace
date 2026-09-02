import uuid

def generate_uuid() -> str:
    """
    Generate a unique UUID4 string.

    Returns:
        str: A unique UUID4 string.
    """
    return str(uuid.uuid4())