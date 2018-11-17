"""Configuration of the tests module."""
import os
import tempfile

import mock
import pytest

from api import create_app
from api.db import init_db
from api.models import CallRecord, PhoneBill, PhoneBillCall


VALID_CALL_RECORD_START = {
    'record_id': 22,
    'record_type': 'start',
    'record_timestamp': '2018-11-11T19:22:16',
    'call_identifier': 1,
    'origin_number': '14981227001',
    'destination_number': '1434567890',
}

VALID_PHONE_BILL = {
    'phone_number': '14981227001',
    'period': '10/2018',
}
INVALID_PHONE_BILL_TYPES = {
    'phone_number': '12312',
    'period': 'anything',
    'record_calls': 'this is not a list',
}

VALID_PHONE_BILL_CALL = {
    'destination_number': '14981227002',
    'call_identifier': 1,
    'call_start': '2018-11-11T19:22:16',
    'call_end': '2018-11-11T19:22:16',
    'bill_call_id': 1,
}


@pytest.fixture
def app():
    """Fixture to return an app instance from the factory."""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Fixture to be used on the tests of the endpoints."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Fixture to be used on CLI tests."""
    return app.test_cli_runner()


@pytest.fixture
@mock.patch('api.models.get_by_id')
def record_start(get_by_id):
    """Fixture to return a valid PhoneCall start object."""
    get_by_id.return_value = None
    return CallRecord(
        VALID_CALL_RECORD_START.get('record_id'),
        VALID_CALL_RECORD_START.get('record_type'),
        VALID_CALL_RECORD_START.get('record_timestamp'),
        VALID_CALL_RECORD_START.get('call_identifier'),
        VALID_CALL_RECORD_START.get('origin_number'),
        VALID_CALL_RECORD_START.get('destination_number'),
    )


@pytest.fixture
@mock.patch('api.models.get_by_id')
def phone_bill(get_by_id):
    """Fixture to return a valid PhoneBill object."""
    get_by_id.return_value = None
    return PhoneBill(
        VALID_PHONE_BILL.get('phone_number'),
        VALID_PHONE_BILL.get('period'),
    )


@pytest.fixture
@mock.patch('api.models.get_by_id')
def invalid_phone_bill(get_by_id):
    """Fixture to return a valid PhoneBill object."""
    get_by_id.return_value = None
    return PhoneBill(
        INVALID_PHONE_BILL_TYPES.get('phone_number'),
        INVALID_PHONE_BILL_TYPES.get('period'),
        INVALID_PHONE_BILL_TYPES.get('record_calls'),
    )


@pytest.fixture
@mock.patch('api.models.get_by_id')
def phone_bill_call(get_by_id):
    """Fixture to return a valid PhoneBill object."""
    get_by_id.return_value = None
    return PhoneBillCall(
        VALID_PHONE_BILL_CALL.get('destination_number'),
        VALID_PHONE_BILL_CALL.get('call_identifier'),
        VALID_PHONE_BILL_CALL.get('call_start'),
        VALID_PHONE_BILL_CALL.get('call_end'),
        bill_call_id=VALID_PHONE_BILL_CALL.get('bill_call_id'),
    )
