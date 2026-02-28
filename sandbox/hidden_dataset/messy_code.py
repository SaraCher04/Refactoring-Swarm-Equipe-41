LOWER_BOUNDARY_EXCLUSIVE = 0
UPPER_BOUNDARY_EXCLUSIVE = 100

def is_strictly_between_boundaries(value: int) -> bool:
    """
    Checks if an integer value is strictly greater than LOWER_BOUNDARY_EXCLUSIVE
    and strictly less than UPPER_BOUNDARY_EXCLUSIVE.

    This means the value must be within the open interval (0, 100),
    i.e., integers from 1 to 99 inclusive.

    Args:
        value: The integer value to check against the defined boundaries.

    Returns:
        True if the value is strictly between the boundaries (0 < value < 100),
        False otherwise.
    """
    return value > LOWER_BOUNDARY_EXCLUSIVE and value < UPPER_BOUNDARY_EXCLUSIVE