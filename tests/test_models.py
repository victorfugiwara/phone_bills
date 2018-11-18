"""Tests for models.py file."""
import mock
import pytest

from datetime import datetime

from api.models import CallRecord, check_exists_id, get_by_id, PhoneBill, PhoneBillCall


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


@mock.patch('api.models.get_by_id')
def test_call_record_validate_end(get_by_id):
    """Test validate function from CallRecord class with valid end data."""
    get_by_id.return_value = None
    obj = CallRecord(
        VALID_CALL_RECORD_END.get('record_id'),
        VALID_CALL_RECORD_END.get('record_type'),
        VALID_CALL_RECORD_END.get('record_timestamp'),
        VALID_CALL_RECORD_END.get('call_identifier'),
    )
    obj.exists_call_id = mock.Mock(return_value=False)

    result = obj.validate()

    assert result == []


@mock.patch('api.models.get_by_id')
def test_call_record_validate_mandatory(get_by_id):
    """Test validate function from CallRecord class with data without mandatory fields."""
    get_by_id.return_value = None
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


@mock.patch('api.models.get_by_id')
def test_call_record_validate_mandatory_start(get_by_id):
    """Test validate function from CallRecord class with data without mandatory fields for start record."""
    get_by_id.return_value = None
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


@mock.patch('api.models.get_by_id')
def test_call_record_validate_types(get_by_id):
    """Test validate function from CallRecord class with invalid data types."""
    get_by_id.return_value = None
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


@mock.patch('api.models.get_by_id')
def test_call_record_validate_types_start(get_by_id):
    """Test validate function from CallRecord class with invalid data types of a start call."""
    get_by_id.return_value = None
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


@mock.patch('api.models.get_by_id')
def test_call_record_exists_call_id_invalid_parameters(get_by_id):
    """Test exists_call_id function from CallRecord class with invalid parameters."""
    get_by_id.return_value = None
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
def test_phone_bill_last_closed_period(tested_date, expected_result, phone_bill):
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
def test_phone_bill_is_valid_period(tested_period, expected_result, phone_bill):
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
def test_phone_bill_is_closed_period(valid_period, value, base_data, expected_result, phone_bill):
    """Test is_closed_period function from PhoneBill class."""
    phone_bill.is_valid_period = mock.Mock(return_value=valid_period)

    result = phone_bill.is_closed_period(value, base_data)

    assert result == expected_result


@pytest.mark.parametrize('phone_number, period', [
    (None, None),
    (None, '11/2018'),
    ('14981227001', None),
])
def test_phone_bill_exists_period_invalid_data(phone_number, period, phone_bill):
    """Test exists_period function from PhoneBill class with invalid data."""
    phone_bill.phone_number = phone_number
    phone_bill.period = period

    result = phone_bill.exists_period()

    assert not result


@mock.patch('api.models.get_db')
def test_phone_bill_exists_period(get_db, phone_bill):
    """Test exists_period function from PhoneBill class."""
    get_db.return_value.cursor.return_value.execute.return_value.fetchone.return_value = {'id': 1}

    result = phone_bill.exists_period()

    assert result
    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        'SELECT id FROM phone_bill WHERE period = ? AND phone_number = ?',
        [phone_bill.period, phone_bill.phone_number]
    )


@mock.patch('api.models.CallRecord')
@mock.patch('api.models.get_db')
def test_phone_bill_get_phone_end_records(get_db, record_class, phone_bill):
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
def test_phone_bill_get_phone_start_records(get_db, record_class, phone_bill):
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


@mock.patch('api.models.get_by_id')
@mock.patch('api.models.PhoneBillCall')
def test_phone_bill_calculate_phone_bill(bill_call_class, get_by_id, phone_bill, record_start):
    """Test calculate_phone_bill function from PhoneBill class."""
    phone_bill.get_phone_end_records = mock.Mock(return_value=[record_start])
    phone_bill.get_phone_start_records = mock.Mock(return_value=[record_start])
    get_by_id.return_value = None
    bill_call_record = PhoneBillCall(
        record_start.destination_number,
        record_start.call_identifier,
        record_start.record_timestamp,
        record_start.record_timestamp
    )
    bill_call_class.return_value = bill_call_record

    phone_bill.calculate_phone_bill()

    phone_bill.get_phone_end_records.assert_called_once()
    phone_bill.get_phone_start_records.assert_called_once_with([1])

    assert phone_bill.record_calls == [bill_call_record]


@mock.patch('api.models.get_db')
def test_phone_bill_save(get_db, phone_bill):
    """Test save function from PhoneBill class."""
    phone_bill.exists_period = mock.Mock(return_value=False)
    get_db.return_value.cursor.return_value.execute.return_value.rowcount = 1

    result = phone_bill.save()

    assert result

    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        'INSERT INTO phone_bill (phone_number, period) VALUES (?, ?)',
        [phone_bill.phone_number, phone_bill.period]
    )


def test_phone_bill_call_to_dict(phone_bill_call):
    """Test to_dict function from PhoneBillCall class."""
    result = phone_bill_call.to_dict()

    assert result == {
        'id': phone_bill_call.id,
        'destination_number': phone_bill_call.destination_number,
        'bill_id': phone_bill_call.bill_id,
        'call_identifier': phone_bill_call.call_identifier,
        'call_start': phone_bill_call.call_start,
        'call_end': phone_bill_call.call_end,
        'duration': phone_bill_call.duration,
        'price': phone_bill_call.price,
    }


def test_phone_bill_call_validate(phone_bill_call):
    """Test validate function from PhoneBillCall class."""
    result = phone_bill_call.validate()

    assert not result


def test_phone_bill_call_validate_mandatory():
    """Test validate function from PhoneBillCall class missing mandatory fields."""
    obj = PhoneBillCall(
        None,
        None,
        None,
        None,
    )

    result = obj.validate()

    assert 'The field destination_number is mandatory.' in result
    assert 'The field call_start is mandatory.' in result
    assert 'The field call_end is mandatory.' in result


@mock.patch('api.models.is_valid_phone_number')
def test_phone_bill_call_validate_invalid(is_valid_phone_number, phone_bill_call):
    """Test validate function from PhoneBillCall class with invalid fields."""
    is_valid_phone_number.return_value = False

    result = phone_bill_call.validate()

    assert 'The field destination_number has an invalid value.' in result


@mock.patch('api.models.check_exists_id')
@mock.patch('api.models.get_db')
def test_phone_bill_call_save_insert(get_db, check_exists_id, phone_bill_call):
    """Test save function from PhoneBillCall class when executes insert."""
    check_exists_id.return_value = False
    get_db.return_value.cursor.return_value.execute.return_value.rowcount = 1

    result = phone_bill_call.save()

    assert result

    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        (
            'INSERT INTO phone_bill_call ('
            'destination_number, call_start, call_end, duration, price, call_identifier, bill_id, id'
            ') VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        ),
        [
            phone_bill_call.destination_number, phone_bill_call.call_start,
            phone_bill_call.call_end, phone_bill_call.duration, phone_bill_call.price,
            phone_bill_call.call_identifier, phone_bill_call.bill_id, phone_bill_call.id
        ]
    )


@mock.patch('api.models.check_exists_id')
@mock.patch('api.models.get_db')
def test_phone_bill_call_save_update(get_db, check_exists_id, phone_bill_call):
    """Test save function from PhoneBillCall class when executes update."""
    check_exists_id.return_value = True
    get_db.return_value.cursor.return_value.execute.return_value.rowcount = 1

    result = phone_bill_call.save()

    assert result

    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        (
            'UPDATE phone_bill_call SET'
            ' destination_number = ?, call_start = ?, call_end = ?, duration = ?,'
            ' price = ?, call_identifier = ?, bill_id = ?'
            ' WHERE id = ?'
        ),
        [
            phone_bill_call.destination_number, phone_bill_call.call_start,
            phone_bill_call.call_end, phone_bill_call.duration, phone_bill_call.price,
            phone_bill_call.call_identifier, phone_bill_call.bill_id, phone_bill_call.id
        ]
    )


def test_check_exists_id_without_id():
    """Test check_exists_id function when id_value is not present on parameters."""
    cursor = mock.Mock()
    table_name = 'table'
    id_field = 'id_of_table'
    id_value = None

    result = check_exists_id(cursor, table_name, id_field, id_value)

    assert not result
    cursor.execute.assert_not_called()


def test_check_exists_id():
    """Test check_exists_id function."""
    cursor = mock.Mock()
    cursor.execute.return_value.fetchone.return_value = [1]
    table_name = 'table'
    id_field = 'id_of_table'
    id_value = 33

    result = check_exists_id(cursor, table_name, id_field, id_value)

    assert result
    cursor.execute.assert_called_once_with('SELECT 1 FROM table WHERE id_of_table = 33')


@mock.patch('api.models.get_db')
def test_get_by_id(get_db):
    """Test get_by_id function."""
    get_db.return_value.cursor.return_value.execute.return_value.fetchone.return_value = {'a': 1}

    table_name = 'table'
    id_field = 'id_of_table'
    id_value = 33

    result = get_by_id(table_name, id_field, id_value)

    assert result

    get_db.return_value.cursor.return_value.execute.assert_called_once_with(
        'SELECT * FROM table WHERE id_of_table = 33'
    )


@mock.patch('api.models.get_db')
def test_get_by_id_without_id(get_db):
    """Test get_by_id function when id_value is not present on parameters."""
    table_name = 'table'
    id_field = 'id_of_table'
    id_value = None

    result = get_by_id(table_name, id_field, id_value)

    assert not result

    get_db.return_value.cursor.return_value.execute.assert_not_called()


@mock.patch('api.models.get_by_id')
def test_calculate_phone_bill_with_data(get_by_id, phone_bill):
    """Test calculate_phone_bill function with a list of record calls mocked."""
    end_records = [
        CallRecord(None, 'end', '2018-10-05T06:00:02', 11),
        CallRecord(None, 'end', '2018-10-09T06:01:00', 12),
        CallRecord(None, 'end', '2018-10-13T00:00:00', 13),
        CallRecord(None, 'end', '2018-10-16T05:59:34', 14),
        CallRecord(None, 'end', '2018-10-18T12:02:45', 15),
        CallRecord(None, 'end', '2018-10-20T23:59:59', 16),
        CallRecord(None, 'end', '2018-10-23T01:59:59', 17),
        CallRecord(None, 'end', '2018-10-25T22:00:00', 18),
        CallRecord(None, 'end', '2018-10-27T22:01:55', 19),
        CallRecord(None, 'end', '2018-10-30T06:30:26', 20)
    ]
    start_records = [
        CallRecord(None, 'start', '2018-10-05T06:00:00', 11, '14981226543', '14998887654'),
        CallRecord(None, 'start', '2018-10-09T06:00:04', 12, '14981226543', '14998887654'),
        CallRecord(None, 'start', '2018-10-12T23:23:23', 13, '14981226543', '1432324455'),
        CallRecord(None, 'start', '2018-10-16T04:54:21', 14, '14981226543', '1432324455'),
        CallRecord(None, 'start', '2018-10-18T12:01:45', 15, '14981226543', '1833445566'),
        CallRecord(None, 'start', '2018-10-20T23:58:59', 16, '14981226543', '1434357263'),
        CallRecord(None, 'start', '2018-10-23T01:00:00', 17, '14981226543', '1432324455'),
        CallRecord(None, 'start', '2018-10-25T19:56:23', 18, '14981226543', '1943536785'),
        CallRecord(None, 'start', '2018-10-27T20:15:55', 19, '14981226543', '1345632789'),
        CallRecord(None, 'start', '2018-10-30T05:30:04', 20, '14981226543', '1345632789')
    ]

    phone_bill.get_phone_end_records = mock.Mock(return_value=end_records)
    phone_bill.get_phone_start_records = mock.Mock(return_value=start_records)
    get_by_id.return_value = None

    phone_bill.calculate_phone_bill()

    assert phone_bill.total == 26.91

    assert phone_bill.record_calls[0].price == 0.36
    assert phone_bill.record_calls[1].price == 0.36
    assert phone_bill.record_calls[2].price == 0.36
    assert phone_bill.record_calls[3].price == 0.36
    assert phone_bill.record_calls[4].price == 0.45
    assert phone_bill.record_calls[5].price == 0.36
    assert phone_bill.record_calls[6].price == 0.36
    assert phone_bill.record_calls[7].price == 11.43
    assert phone_bill.record_calls[8].price == 9.72
    assert phone_bill.record_calls[9].price == 3.15
