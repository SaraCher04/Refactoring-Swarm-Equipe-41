def count_down(n: int) -> None:
    """
    Counts down from a given positive integer 'n' to 1, printing each number.

    Args:
        n: The starting integer for the countdown.

    Raises:
        ValueError: If 'n' is not an integer or is a boolean.
    """
    if isinstance(n, bool):  # Check for boolean specifically, as bool is a subclass of int
        raise ValueError("Input 'n' must be an integer, not a boolean.")
    if not isinstance(n, int):
        raise ValueError("Input 'n' must be an integer.")
    if n <= 0:
        print(f"Countdown starts from {n}. No numbers > 0 to count down.")
        return

    print(f"Starting countdown from {n}:")
    while n > 0:
        print(n)
        n -= 1