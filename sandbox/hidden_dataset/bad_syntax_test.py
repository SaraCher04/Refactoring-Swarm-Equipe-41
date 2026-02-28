import pytest
from bad_syntax import calculate_sum

def test_calculate_sum_positive_integers():
    assert calculate_sum(2, 3) == 5

def test_calculate_sum_negative_integers():
    assert calculate_sum(-2, -3) == -5

def test_calculate_sum_mixed_integers():
    assert calculate_sum(5, -3) == 2
    assert calculate_sum(-5, 3) == -2

def test_calculate_sum_positive_floats():
    assert calculate_sum(2.5, 3.5) == 6.0

def test_calculate_sum_negative_floats():
    assert calculate_sum(-2.5, -3.5) == -6.0

def test_calculate_sum_mixed_floats():
    assert calculate_sum(5.5, -3.0) == 2.5
    assert calculate_sum(-5.5, 3.0) == -2.5

def test_calculate_sum_integer_and_float():
    assert calculate_sum(2, 3.5) == 5.5
    assert calculate_sum(3.5, 2) == 5.5
    assert calculate_sum(-2, 3.5) == 1.5
    assert calculate_sum(2, -3.5) == -1.5

def test_calculate_sum_with_zero():
    assert calculate_sum(0, 5) == 5
    assert calculate_sum(5, 0) == 5
    assert calculate_sum(0, 0) == 0
    assert calculate_sum(0.0, 5.0) == 5.0
    assert calculate_sum(5.0, 0.0) == 5.0
    assert calculate_sum(0.0, 0.0) == 0.0
    assert calculate_sum(0, -5) == -5
    assert calculate_sum(-5, 0) == -5
    assert calculate_sum(0.0, -5.0) == -5.0
    assert calculate_sum(-5.0, 0.0) == -5.0

def test_calculate_sum_large_numbers():
    assert calculate_sum(1_000_000_000, 2_000_000_000) == 3_000_000_000
    assert calculate_sum(1e18, 2e18) == pytest.approx(3e18)

def test_calculate_sum_small_floats_precision():
    assert calculate_sum(0.1, 0.2) == pytest.approx(0.3)
    assert calculate_sum(0.0000001, 0.0000002) == pytest.approx(0.0000003)

def test_calculate_sum_extreme_values():
    assert calculate_sum(1e-20, 2e-20) == pytest.approx(3e-20)
    assert calculate_sum(1e300, 1e300) == pytest.approx(2e300)
    assert calculate_sum(-1e300, 1e300) == pytest.approx(0.0)