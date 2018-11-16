"""Utils functions used to help in common operations."""
from datetime import datetime


def get_date_or_none(value):
    """
    Return the value converted as datetime type or None.

    Args:
        value (any): Value to be converted to a datetime object.

    Returns:
        (datetime/None): When is possible to convert the value in a datetime the function
            will return the datetime object. If not will return None.
    """
    if not value:
        return None

    if isinstance(value, datetime):
        return value

    if isinstance(value, str):
        formats = ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%SZ']
        for convert_format in formats:
            try:
                return datetime.strptime(value, convert_format)
            except (ValueError, TypeError):
                pass

    return None


def get_int_or_none(value):
    """
    Return the value converted as integer type or None.

    Args:
        value (any): Value to be converted to a integer.

    Returns:
        (integer/None): When is possible to convert the value in a integer the function
            will return the integer object. If not will return None.
    """
    if not value:
        return None

    if isinstance(value, int):
        return value

    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def is_valid_phone_number(number):
    """Check if the phone number is in the valid format."""
    if not number:
        return False

    return 10 <= len(str(number)) <= 11
