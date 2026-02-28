import pytest
import io
import sys
from logic_bug import count_down

def test_count_down_positive_number(capfd):
    count_down(3)
    captured = capfd.readouterr()
    expected_output = "Starting countdown from 3:\n3\n2\n1\n"
    assert captured.out == expected_output
    assert captured.err == ""

def test_count_down_one(capfd):
    count_down(1)
    captured = capfd.readouterr()
    expected_output = "Starting countdown from 1:\n1\n"
    assert captured.out == expected_output
    assert captured.err == ""

def test_count_down_zero(capfd):
    count_down(0)
    captured = capfd.readouterr()
    expected_output = "Countdown starts from 0. No numbers > 0 to count down.\n"
    assert captured.out == expected_output
    assert captured.err == ""

def test_count_down_negative_number(capfd):
    count_down(-5)
    captured = capfd.readouterr()
    expected_output = "Countdown starts from -5. No numbers > 0 to count down.\n"
    assert captured.out == expected_output
    assert captured.err == ""

def test_count_down_non_integer_float():
    with pytest.raises(ValueError) as excinfo:
        count_down(3.5)
    assert str(excinfo.value) == "Input 'n' must be an integer."

def test_count_down_non_integer_string():
    with pytest.raises(ValueError) as excinfo:
        count_down("hello")
    assert str(excinfo.value) == "Input 'n' must be an integer."

def test_count_down_non_integer_none():
    with pytest.raises(ValueError) as excinfo:
        count_down(None)
    assert str(excinfo.value) == "Input 'n' must be an integer."

def test_count_down_non_integer_boolean():
    with pytest.raises(ValueError) as excinfo:
        count_down(True) # Booleans are technically integers (1 and 0), but the function expects an int that behaves like a number for countdown. This case is covered by the type check.
    assert str(excinfo.value) == "Input 'n' must be an integer."

def test_count_down_large_number(capfd):
    # Test with a slightly larger number to ensure loop behavior
    count_down(5)
    captured = capfd.readouterr()
    expected_output = "Starting countdown from 5:\n5\n4\n3\n2\n1\n"
    assert captured.out == expected_output
    assert captured.err == ""