"""Tests for models.py file."""
import mock
import pytest

from datetime import datetime

from api.models import CallRecord, PhoneBill


VALID_CALL_RECORD_START = {
    'record_id': 22,
    'record_type': 'start',
    'record_timestamp': '2018-11-11T19:22:16',
    'call_identifier': 1,
    'origin_number': '14981227001',
    'destination_number': '1434567890',
}
VALID_CALL_RECORD_END = {
    'record_id': 25,
    'record_type': 'end',
    'record_timestamp': '2018-11-11T20:03:43',
    'call_identifier': 1,
}

INVALID_CALL_RECORD_WITHOUT_MANDATORY = {
    'record_id': 22,
    'record_timestamp': '2018-11-11T20:03:43',
}
INVALID_CALL_RECORD_WITHOUT_MANDATORY_START = {
    'record_id': 22,
    'record_timestamp': '2018-11-11T20:03:43',
    'record_type': 'start',
}
INVALID_CALL_RECORD_TYPES = {
    'record_id': 22,
    'record_type': 'other',
    'record_timestamp': 'not a date',
    'call_identifier': 1,
}
INVALID_CALL_RECORD_TYPES_START = {
    'record_id': 22,
    'record_type': 'start',
    'record_timestamp': 'not a date',
    'call_identifier': 1,
    'origin_number': '12345',
    'destination_number': '1111',
}

VALID_PHONE_BILL = {
    'phone_number': '14981227001',
    'period': '10/2018',
}


def test_call_record_validate_start(record_start):
    """Test validate function from CallRecord class with valid start data."""
    record_start.exists_call_id = mock.Mock(return_value=False)

    result = record_start.validate()

    assert result == []


def test_call_record_validate_end():
    """Test validate function from CallRecord class with valid end data."""
    obj = CallRecord(
        VALID_CALL_RECORD_END.get('record_id'),
        VALID_CALL_RECORD_END.get('record_type'),
        VALID_CALL_RECORD_END.get('record_timestamp'),
        VALID_CALL_RECORD_END.get('call_identifier'),
    )
    obj.exists_call_id = mock.Mock(return_value=False)

    result = obj.validate()

    assert result == []


def test_call_record_validate_mandatory():
    """Test validate function from CallRecord class with data without mandatory fields."""
    obj = CallRecord(
        INVALID_CALL_RECORD_WITHOUT_MANDATORY.get('record_id'),
        INVALID_CALL_RECORD_WITHOUT_MANDATORY.get('record_type'),
        INVALID_CALL_RECORD_WITHOUT_MANDATORY.get('record_timestamp'),
        INVALID_CALL_RECORD_WITHOUT_MANDATORY.get('call_identifier'),
        INVALID_CALL_RECORD_WITHOUT_MANDATORY.get('origin_number'),
        INVALID_CALL_RECORD_WITHOUT_MANDATORY.get('destination_number'),
    )
    obj.exists_call_id = mock.Mock(return_value=False)

    result = obj.validate()

    assert 'The field record_type is mandatory.' in result
    assert 'The field call_identifier is mandatory.' in result


def test_call_record_validate_mandatory_start():
    """Test validate function from CallRecord class with data without mandatory fields for start record."""
    obj = CallRecord(
        INVALID_CALL_RECORD_WITHOUT_MANDATORY_START.get('record_id'),
        INVALID_CALL_RECORD_WITHOUT_MANDATORY_START.get('record_type'),
        INVALID_CALL_RECORD_WITHOUT_MANDATORY_START.get('record_timestamp'),
        INVALID_CALL_RECORD_WITHOUT_MANDATORY_START.get('call_identifier'),
        INVALID_CALL_RECORD_WITHOUT_MANDATORY_START.get('origin_number'),
        INVALID_CALL_RECORD_WITHOUT_MANDATORY_START.get('destination_number'),
    )
    obj.exists_call_id = mock.Mock(return_value=False)

    result = obj.validate()

    assert 'The field call_identifier is mandatory.' in result
    assert 'The field origin_number is mandatory.' in result
    assert 'The field destination_number is mandatory.' in result


def test_call_record_validate_types():
    """Test validate function from CallRecord class with invalid data types."""
    obj = CallRecord(
        INVALID_CALL_RECORD_TYPES.get('record_id'),
        INVALID_CALL_RECORD_TYPES.get('record_type'),
        INVALID_CALL_RECORD_TYPES.get('record_timestamp'),
        INVALID_CALL_RECORD_TYPES.get('call_identifier'),
        INVALID_CALL_RECORD_TYPES.get('origin_number'),
        INVALID_CALL_RECORD_TYPES.get('destination_number'),
    )
    obj.exists_call_id = mock.Mock(return_value=False)

    result = obj.validate()

    assert 'The field record_type has an invalid value.' in result
    assert 'The field record_timestamp has an invalid value.' in result


def test_call_record_validate_types_start():
    """Test validate function from CallRecord class with invalid data types of a start call."""
    obj = CallRecord(
        INVALID_CALL_RECORD_TYPES_START.get('record_id'),
        INVALID_CALL_RECORD_TYPES_START.get('record_type'),
        INVALID_CALL_RECORD_TYPES_START.get('record_timestamp'),
        INVALID_CALL_RECORD_TYPES_START.get('call_identifier'),
        INVALID_CALL_RECORD_TYPES_START.get('origin_number'),
        INVALID_CALL_RECORD_TYPES_START.get('destination_number'),
    )
    obj.exists_call_id = mock.Mock(return_value=False)

    result = obj.validate()

    assert 'The field record_timestamp has an invalid value.' in result
    assert 'The field origin_number has an invalid value.' in result
    assert 'The field destination_number has an invalid value.' in result


def test_call_record_validate_duplicated(record_start):
    """Test validate function from CallRecord class with invalid data types of a start call."""
    record_start.exists_call_id = mock.Mock(return_value=True)

    result = record_start.validate()
    duplicate_msg = 'Database already has a record with given call id {} record type {} with other record id.'.format(
        record_start.call_identifier,
        record_start.record_type
    )
    assert duplicate_msg in result


def test_call_record_exists_call_id_invalid_parameters():
    """Test exists_call_id function from CallRecord class with invalid parameters."""
    obj = CallRecord(
        VALID_CALL_RECORD_START.get('record_id'),
        VALID_CALL_RECORD_START.get('record_type'),
        VALID_CALL_RECORD_START.get('record_timestamp'),
        None,
        VALID_CALL_RECORD_START.get('origin_number'),
        VALID_CALL_RECORD_START.get('destination_number'),
    )

    result = obj.exists_call_id()

    assert not result


@mock.patch('api.models.get_db')
def test_call_record_exists_call_id_invalid_without_record_id(get_db):
    """Test exists_call_id function from CallRecord class without record_id."""
    obj = CallRecord(
        None,
        VALID_CALL_RECORD_START.get('record_type'),
        VALID_CALL_RECORD_START.get('record_timestamp'),
        VALID_CALL_RECORD_START.get('call_identifier'),
        VALID_CALL_RECORD_START.get('origin_number'),
        VALID_CALL_RECORD_START.get('destination_number'),
    )

    get_db.return_value.cursor.return_value.execute.return_value.fetchone.return_value = None

    result = obj.exists_call_id()

    assert not result
    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        'SELECT 1 FROM phone_call WHERE call_identifier = 1 AND record_type = ?',
        [obj.record_type]
    )


@mock.patch('api.models.get_db')
def test_call_record_exists_call_id_invalid_with_record_id(get_db, record_start):
    """Test exists_call_id function from CallRecord class with record_id."""
    get_db.return_value.cursor.return_value.execute.return_value.fetchone.return_value = None

    result = record_start.exists_call_id()

    assert not result
    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        'SELECT 1 FROM phone_call WHERE call_identifier = 1 AND record_type = ? AND record_id <> 22',
        [record_start.record_type]
    )


@mock.patch('api.models.check_exists_id')
@mock.patch('api.models.get_db')
def test_call_record_save_insert(get_db, check_exists_id, record_start):
    """Test save function from CallRecord class when executes insert."""
    check_exists_id.return_value = False
    get_db.return_value.cursor.return_value.execute.return_value.rowcount = 1

    result = record_start.save()

    assert result

    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        (
            'INSERT INTO phone_call ('
            'record_type, record_timestamp, call_identifier, origin_number,'
            ' destination_number, record_id) VALUES (?, ?, ?, ?, ?, ?)'
        ),
        [
            record_start.record_type, record_start.record_timestamp, record_start.call_identifier,
            record_start.origin_number, record_start.destination_number, record_start.record_id
        ]
    )


@mock.patch('api.models.check_exists_id')
@mock.patch('api.models.get_db')
def test_call_record_save_update(get_db, check_exists_id, record_start):
    """Test save function from CallRecord class when executes update."""
    check_exists_id.return_value = True
    get_db.return_value.cursor.return_value.execute.return_value.rowcount = 1

    result = record_start.save()

    assert result

    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        (
            'UPDATE phone_call SET'
            ' record_type = ?, record_timestamp = ?, call_identifier = ?,'
            ' origin_number = ?, destination_number = ?'
            ' WHERE record_id = ?'
        ),
        [
            record_start.record_type, record_start.record_timestamp, record_start.call_identifier,
            record_start.origin_number, record_start.destination_number, record_start.record_id
        ]
    )


def test_phone_bill_validate(phone_bill):
    """Test validate function from PhoneBill class with valid data."""
    result = phone_bill.validate()

    assert result == []


def test_phone_bill_validate_mandatory():
    """Test validate function from PhoneBill class with data without mandatory fields."""
    obj = PhoneBill(
        None,
    )

    result = obj.validate()

    assert 'The field phone_number is mandatory.' in result


def test_phone_bill_validate_types(invalid_phone_bill):
    """Test validate function from PhoneBill class with invalid data types."""
    result = invalid_phone_bill.validate()

    assert 'The field phone_number has an invalid value.' in result
    assert 'The field period has an invalid value.' in result
    assert 'The field record_calls has an invalid value.' in result


def test_phone_bill_exists_period_invalid_without_parameter(phone_bill):
    """Test exists_period function from PhoneBill class without parameters."""
    phone_bill.period = None
    phone_bill.phone_number = None

    result = phone_bill.exists_period()

    assert not result


@mock.patch('api.models.get_db')
def test_phone_bill_exists_period(get_db, phone_bill):
    """Test exists_period function from PhoneBill class."""
    get_db.return_value.cursor.return_value.execute.return_value.fetchone.return_value = (1)

    result = phone_bill.exists_period()

    assert result
    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        'SELECT 1 FROM phone_bill WHERE period = ? AND phone_number = ?',
        [phone_bill.period, phone_bill.phone_number]
    )


def test_phone_bill_to_dict():
    """Test to_dict function from PhoneBill class."""
    record_to_dict = mock.Mock()
    record_to_dict.to_dict.return_value = {'record': 'value'}
    obj = PhoneBill(
        VALID_PHONE_BILL.get('phone_number'),
        VALID_PHONE_BILL.get('period'),
        [record_to_dict]
    )

    result = obj.to_dict()

    assert result == {
        'subscriber': obj.phone_number,
        'period': obj.period,
        'total': obj.total,
        'calls': [record_to_dict.to_dict.return_value],
    }


@pytest.mark.parametrize('tested_date, expected_result', [
    (datetime(2018, 1, 1), '12/2017'),
    (datetime(2018, 1, 31), '12/2017'),
    (datetime(2018, 2, 2), '01/2018'),
    (datetime(2018, 3, 1), '02/2018'),
    (datetime(2018, 11, 30), '10/2018'),
    (datetime(2018, 12, 31), '11/2018'),
    (datetime(2019, 1, 1), '12/2018'),
])
def test_last_closed_period(tested_date, expected_result, phone_bill):
    """Test last_closed_period function from PhoneBill class."""
    result = phone_bill.last_closed_period(tested_date)

    assert result == expected_result


@pytest.mark.parametrize('tested_period, expected_result', [
    (None, False),
    ('15/05/2018', False),
    ('5', False),
    ('0/0', False),
    ('0/2018', False),
    ('-50/2018', False),
    ('33/2018', False),
    ('13/2018', False),
    ('12 / 2017', True),
    ('1/2018', True),
    ('12/2018', True),
])
def test_is_valid_period(tested_period, expected_result, phone_bill):
    """Test is_valid_period function from PhoneBill class."""
    result = phone_bill.is_valid_period(tested_period)

    assert result == expected_result


@pytest.mark.parametrize('valid_period, value, base_data, expected_result', [
    (False, 'any', 'any', False),
    (True, '01/2018', datetime(2018, 1, 1), False),
    (True, '01/2018', datetime(2018, 2, 1), True),
    (True, '12/2018', datetime(2018, 12, 1), False),
    (True, '12/2018', datetime(2018, 12, 31), False),
    (True, '12/2018', datetime(2019, 1, 1), True),
    (True, '01/2018', datetime(2018, 11, 14), True),
])
def test_is_closed_period(valid_period, value, base_data, expected_result, phone_bill):
    """Test is_closed_period function from PhoneBill class."""
    phone_bill.is_valid_period = mock.Mock(return_value=valid_period)

    result = phone_bill.is_closed_period(value, base_data)

    assert result == expected_result


@pytest.mark.parametrize('phone_number, period', [
    (None, None),
    (None, '11/2018'),
    ('14981227001', None),
])
def test_exists_period_invalid_data(phone_number, period, phone_bill):
    """Test exists_period function from PhoneBill class with invalid data."""
    phone_bill.phone_number = phone_number
    phone_bill.period = period

    result = phone_bill.exists_period()

    assert not result


@mock.patch('api.models.get_db')
def test_exists_period(get_db, phone_bill):
    """Test exists_period function from PhoneBill class."""
    get_db.return_value.cursor.return_value.execute.return_value.fetchone.return_value = {}

    result = phone_bill.exists_period()

    assert result
    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        'SELECT 1 FROM phone_bill WHERE period = ? AND phone_number = ?',
        [phone_bill.period, phone_bill.phone_number]
    )


@mock.patch('api.models.CallRecord')
@mock.patch('api.models.get_db')
def test_get_phone_end_records(get_db, record_class, phone_bill):
    """Test get_phone_end_records function from PhoneBill class."""
    records_found = [
        ['A', 'B', 'C', 'D', 'E', 'F'],
        ['U', 'V', 'W', 'X', 'Y', 'Z'],
    ]
    get_db.return_value.cursor.return_value.execute.return_value.fetchall.return_value = records_found
    record_class.TABLE_NAME = 'phone_call'

    result = phone_bill.get_phone_end_records()

    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        'SELECT'
        ' record_id, record_type, record_timestamp, call_identifier, origin_number, destination_number'
        ' FROM phone_call WHERE'
        ' record_type = ? AND'
        ' strftime(?, record_timestamp) = ? AND'
        ' strftime(?, record_timestamp) = ?',
        ['end', '%m', '10', '%Y', '2018']
    )

    record_class.assert_has_calls([
        mock.call(
            records_found[0][0],
            records_found[0][1],
            records_found[0][2],
            records_found[0][3],
            records_found[0][4],
            records_found[0][5]
        ),
        mock.call(
            records_found[1][0],
            records_found[1][1],
            records_found[1][2],
            records_found[1][3],
            records_found[1][4],
            records_found[1][5]
        ),
    ])

    assert result == [
        record_class(
            records_found[0][0],
            records_found[0][1],
            records_found[0][2],
            records_found[0][3],
            records_found[0][4],
            records_found[0][5]
        ),
        record_class(
            records_found[1][0],
            records_found[1][1],
            records_found[1][2],
            records_found[1][3],
            records_found[1][4],
            records_found[1][5]
        ),
    ]


@mock.patch('api.models.CallRecord')
@mock.patch('api.models.get_db')
def test_get_phone_start_records(get_db, record_class, phone_bill):
    """Test get_phone_start_records function from PhoneBill class."""
    records_found = [
        ['A', 'B', 'C', 'D', 'E', 'F'],
        ['U', 'V', 'W', 'X', 'Y', 'Z'],
    ]
    get_db.return_value.cursor.return_value.execute.return_value.fetchall.return_value = records_found
    record_class.TABLE_NAME = 'phone_call'
    calls_ids = [1, 2, 3]

    result = phone_bill.get_phone_start_records(calls_ids)

    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        'SELECT record_id, record_type, record_timestamp, call_identifier, origin_number, destination_number '
        'FROM phone_call WHERE'
        ' record_type = ? AND'
        ' call_identifier IN (1, 2, 3)',
        ['start']
    )

    record_class.assert_has_calls([
        mock.call(
            records_found[0][0], records_found[0][1], records_found[0][2],
            records_found[0][3], records_found[0][4], records_found[0][5]
        ),
        mock.call(
            records_found[1][0], records_found[1][1], records_found[1][2],
            records_found[1][3], records_found[1][4], records_found[1][5]
        ),
    ])

    assert result == [
        record_class(
            records_found[0][0], records_found[0][1], records_found[0][2],
            records_found[0][3], records_found[0][4], records_found[0][5]
        ),
        record_class(
            records_found[1][0], records_found[1][1], records_found[1][2],
            records_found[1][3], records_found[1][4], records_found[1][5]
        ),
    ]


def test_calculate_phone_bill(phone_bill, record_start):
    """Test calculate_phone_bill function from PhoneBill class."""
    phone_bill.get_phone_end_records = mock.Mock(return_value=[record_start])
    phone_bill.get_phone_start_records = mock.Mock(return_value=[record_start])

    phone_bill.calculate_phone_bill()

    phone_bill.get_phone_end_records.assert_called_once()
    phone_bill.get_phone_start_records.assert_called_once_with([1])
