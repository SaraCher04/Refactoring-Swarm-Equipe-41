import pytest
from messy_code import LOWER_BOUNDARY_EXCLUSIVE, UPPER_BOUNDARY_EXCLUSIVE, is_strictly_between_boundaries

@pytest.mark.parametrize("value", [
    LOWER_BOUNDARY_EXCLUSIVE + 1,
    UPPER_BOUNDARY_EXCLUSIVE - 1,
    50,
    1,
    99,
    10,
    90,
])
def test_is_strictly_between_boundaries_true_cases(value):
    assert is_strictly_between_boundaries(value) is True

@pytest.mark.parametrize("value", [
    LOWER_BOUNDARY_EXCLUSIVE,
    UPPER_BOUNDARY_EXCLUSIVE,
    LOWER_BOUNDARY_EXCLUSIVE - 1,
    UPPER_BOUNDARY_EXCLUSIVE + 1,
    -10,
    150,
    -1000,
    1000,
])
def test_is_strictly_between_boundaries_false_cases(value):
    assert is_strictly_between_boundaries(value) is False