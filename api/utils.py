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
        try:
            return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        except (ValueError, TypeError):
            pass

    return None
