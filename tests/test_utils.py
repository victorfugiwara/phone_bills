"""Tests for utils.py file."""
from datetime import datetime
import pytest

from api import utils


@pytest.mark.parametrize('value, expected_result', [
    (None, None),
    ('', None),
    (datetime(2018, 11, 10), datetime(2018, 11, 10)),
    ('2018-11-10T13:45:33', datetime(2018, 11, 10, 13, 45, 33)),
    ('2000-1-1T1:1:1', datetime(2000, 1, 1, 1, 1, 1)),
    ('not a date', None),
])
def test_get_date_or_none(value, expected_result):
    """Test get_date_or_none function."""
    result = utils.get_date_or_none(value)
    assert result == expected_result


@pytest.mark.parametrize('value, expected_result', [
    (None, None),
    ('', None),
    (1, 1),
    ('7', 7),
    ('10', 10),
    ('005', 5),
    ('4d4g', None),
])
def test_get_int_or_none(value, expected_result):
    """Test get_int_or_none function."""
    result = utils.get_int_or_none(value)
    assert result == expected_result


@pytest.mark.parametrize('number, expected_result', [
    (None, False),
    ('', False),
    (0, False),
    (123456789, False),
    (1234567890, True),
    (12345678901, True),
    (123456789012, False),
    ('123456789', False),
    ('1234567890', True),
    ('12345678901', True),
    ('123456789012', False),
])
def test_is_valid_phone_number(number, expected_result):
    """Test is_valid_phone_number function."""
    result = utils.is_valid_phone_number(number)
    assert result == expected_result
