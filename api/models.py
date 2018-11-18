"""Models of data used in the api."""
from datetime import datetime, timedelta

from api import constants
from api.db import get_db
from api.utils import get_date_or_none, get_int_or_none, is_valid_phone_number


class CallRecord:
    """Model to store phone call records."""

    TABLE_NAME = 'phone_call'

    def __init__(
        self, record_id, record_type, record_timestamp, call_identifier, origin_number=None, destination_number=None
    ):
        """Constructor used to populate the data of the object."""
        if record_id:
            existent = get_by_id(
                self.TABLE_NAME,
                'record_id',
                record_id,
                ['record_type', 'record_timestamp', 'call_identifier', 'origin_number', 'destination_number']
            )
            if existent:
                self.record_id = record_id
                self.record_type = existent.get('record_type')
                self.record_timestamp = existent.get('record_timestamp')
                self.call_identifier = existent.get('call_identifier')
                self.origin_number = existent.get('origin_number')
                self.destination_number = existent.get('destination_number')
                return

        self.record_id = record_id
        self.record_type = record_type
        self.record_timestamp = get_date_or_none(record_timestamp)
        self.call_identifier = call_identifier
        self.origin_number = origin_number
        self.destination_number = destination_number

    def validate(self):
        """
        Validate if the mandatory fields are present and are valid.

        Returns:
            (list): list of error messages generated by the validation.
        """
        error_messages = []

        if not self.record_type:
            error_messages.append(constants.MESSAGE_MANDATORY_FIELD.format('record_type'))
        elif self.record_type not in constants.RECORD_TYPE_OPTIONS:
            error_messages.append(constants.MESSAGE_INVALID_FIELD.format('record_type'))

        if not self.record_timestamp:
            error_messages.append(constants.MESSAGE_INVALID_FIELD.format('record_timestamp'))

        if not self.call_identifier:
            error_messages.append(constants.MESSAGE_MANDATORY_FIELD.format('call_identifier'))

        if self.record_type and self.record_type == constants.RECORD_TYPE_START:
            if not self.origin_number:
                error_messages.append(constants.MESSAGE_MANDATORY_FIELD.format('origin_number'))
            elif not is_valid_phone_number(self.origin_number):
                error_messages.append(constants.MESSAGE_INVALID_FIELD.format('origin_number'))

            if not self.destination_number:
                error_messages.append(constants.MESSAGE_MANDATORY_FIELD.format('destination_number'))
            elif not is_valid_phone_number(self.destination_number):
                error_messages.append(constants.MESSAGE_INVALID_FIELD.format('destination_number'))

        if self.call_identifier and self.record_type and self.exists_call_id():
            error_messages.append(constants.MESSAGE_DUPLICATED_CALL_ID.format(self.call_identifier, self.record_type))

        return error_messages

    def exists_call_id(self):
        """Check if already exists a record with the call_id and record_type."""
        if not self.call_identifier or not self.record_type:
            return False

        sql_command = 'SELECT 1 FROM {} WHERE call_identifier = {} AND record_type = ?'.format(
            self.TABLE_NAME, self.call_identifier
        )
        if self.record_id:
            sql_command += ' AND record_id <> {}'.format(self.record_id)
        cursor = get_db().cursor()
        result = cursor.execute(sql_command, [self.record_type])

        return result.fetchone() is not None

    def save(self):
        """Save the Call Record data on the database."""
        db = get_db()
        cursor = db.cursor()

        exists_id = check_exists_id(cursor, self.TABLE_NAME, 'record_id', self.record_id)

        if exists_id:
            update = 'record_type = ?, record_timestamp = ?, call_identifier = ?'
            if self.record_type == constants.RECORD_TYPE_START:
                update += ', origin_number = ?, destination_number = ?'

            sql_command = 'UPDATE {} SET {} WHERE record_id = ?'.format(self.TABLE_NAME, update)
        else:
            fields = ['record_type', 'record_timestamp', 'call_identifier']
            if self.record_type == constants.RECORD_TYPE_START:
                fields.append('origin_number')
                fields.append('destination_number')
            if self.record_id:
                fields.append('record_id')

            sql_command = 'INSERT INTO {} ({}) VALUES ({})'.format(
                self.TABLE_NAME,
                ', '.join(fields),
                ', '.join(['?'] * len(fields))
            )

        values = [self.record_type, self.record_timestamp, self.call_identifier]
        if self.record_type == constants.RECORD_TYPE_START:
            values.append(self.origin_number)
            values.append(self.destination_number)
        if self.record_id:
            values.append(self.record_id)

        res = cursor.execute(sql_command, values)
        db.commit()

        return res.rowcount > 0


class PhoneBill:
    """Model to store phone bills."""

    TABLE_NAME = 'phone_bill'

    def __init__(self, phone_number, period=None, record_calls=None, bill_id=None):
        """Constructor used to populate the data of the object."""
        self.phone_number = phone_number
        if period:
            self.period = period
        else:
            self.period = self.last_closed_period(datetime.today())
        if record_calls:
            self.record_calls = record_calls
        else:
            self.record_calls = []

        self.total = 0
        self.id = bill_id

    def to_dict(self):
        """Format the object in a json document."""
        calls_dict = []
        for record in self.record_calls:
            calls_dict.append(record.to_dict())
        return {
            'subscriber': self.phone_number,
            'period': self.period,
            'total': self.total,
            'calls': calls_dict
        }

    def last_closed_period(self, base_date):
        """Return the last closed period based on the current date."""
        first_day = '{}/{}'.format(base_date.year, base_date.month)
        first_day = datetime.strptime(first_day, '%Y/%m')
        first_day = first_day - timedelta(days=1)

        return '{:02}/{:0004}'.format(first_day.month, first_day.year)

    def validate(self):
        """
        Validate if the mandatory fields are present and are valid.

        Returns:
            (list): list of error messages generated by the validation.
        """
        error_messages = []

        if not self.phone_number:
            error_messages.append(constants.MESSAGE_MANDATORY_FIELD.format('phone_number'))
        elif not is_valid_phone_number(self.phone_number):
            error_messages.append(constants.MESSAGE_INVALID_FIELD.format('phone_number'))

        if self.period and not self.is_valid_period(self.period):
            error_messages.append(constants.MESSAGE_INVALID_FIELD.format('period'))
        elif self.period and not self.is_closed_period(self.period, datetime.today()):
            error_messages.append(constants.MESSAGE_INVALID_PERIOD.format('period'))

        if self.record_calls and not isinstance(self.record_calls, list):
            error_messages.append(constants.MESSAGE_INVALID_FIELD.format('record_calls'))

        return error_messages

    def is_valid_period(self, value):
        """Check if the value is a valid period format. Should be month/year."""
        if not value:
            return False

        splitted = value.split('/')
        if not len(splitted) == 2:
            return False

        month = get_int_or_none(splitted[0])
        year = get_int_or_none(splitted[1])

        if not month or not year:
            return False

        if not 1 <= month <= 12:
            return False

        return True

    def is_closed_period(self, value, base_date):
        """Check if the period is a closed month lower than today."""
        if not self.is_valid_period(value):
            return False

        splitted = value.split('/')
        month = get_int_or_none(splitted[0])
        year = get_int_or_none(splitted[1])

        if base_date.year < year or base_date.year == year and base_date.month <= month:
            return False

        return True

    def exists_period(self):
        """Check if already exists a record with the period."""
        if not self.period or not self.phone_number:
            return False

        sql_command = 'SELECT id FROM {} WHERE period = ? AND phone_number = ?'.format(self.TABLE_NAME)
        cursor = get_db().cursor()
        result = cursor.execute(sql_command, [self.period, self.phone_number]).fetchone()

        return result['id'] if result else None

    def get_phone_end_records(self):
        """Return the existent list of record calls. If it is empty, will calculate."""
        splitted = self.period.split('/')
        month = '{:02}'.format(get_int_or_none(splitted[0]))
        year = '{:0004}'.format(get_int_or_none(splitted[1]))

        sql_command = (
            'SELECT'
            ' record_id, record_type, record_timestamp, call_identifier, origin_number, destination_number'
            ' FROM {} WHERE'
            ' record_type = ? AND'
            ' strftime(?, record_timestamp) = ? AND'
            ' strftime(?, record_timestamp) = ?'
        ).format(CallRecord.TABLE_NAME)

        cursor = get_db().cursor()
        result = cursor.execute(sql_command, ['end', '%m', month, '%Y', year])

        end_record_calls = []
        for record in result.fetchall():
            end_record_calls.append(CallRecord(
                record[0],
                record[1],
                record[2],
                record[3],
                record[4],
                record[5]
            ))

        return end_record_calls

    def get_phone_start_records(self, calls_ids):
        """Retrieve from the database the start records of the calls_ids."""
        if not calls_ids:
            return []

        sql_command = (
            'SELECT record_id, record_type, record_timestamp, call_identifier, origin_number, destination_number '
            'FROM {} WHERE'
            ' record_type = ? AND'
            ' call_identifier IN ({})'
        ).format(CallRecord.TABLE_NAME, ', '.join([str(item) for item in calls_ids]))

        cursor = get_db().cursor()
        result = cursor.execute(sql_command, ['start'])

        start_records = []
        for record in result.fetchall():
            start_records.append(CallRecord(
                record[0],
                record[1],
                record[2],
                record[3],
                record[4],
                record[5]
            ))

        return start_records

    def calculate_phone_bill(self):
        """Calculate the price of the phone bill."""
        self.total = 0
        phone_end_records = self.get_phone_end_records()
        calls_ids = [c.call_identifier for c in phone_end_records]
        dict_start_records = {
            call.call_identifier: call for call in self.get_phone_start_records(calls_ids)
        }

        standard_initial_hours = int(constants.STANDARD_INITIAL_TIME.split(':')[0])
        standard_initial_minutes = int(constants.STANDARD_INITIAL_TIME.split(':')[1])
        standard_final_hours = int(constants.STANDARD_FINAL_TIME.split(':')[0])
        standard_final_minutes = int(constants.STANDARD_FINAL_TIME.split(':')[1])

        reduced_final_hours = int(constants.REDUCED_FINAL_TIME.split(':')[0])
        reduced_final_minutes = int(constants.REDUCED_FINAL_TIME.split(':')[1])

        for end_record in phone_end_records:
            start_record = dict_start_records.get(end_record.call_identifier)
            if not start_record:
                continue
            phone_bill_call = PhoneBillCall(
                start_record.destination_number,
                start_record.call_identifier,
                start_record.record_timestamp,
                end_record.record_timestamp
            )
            if phone_bill_call.id:
                self.total += phone_bill_call.price
                self.record_calls.append(phone_bill_call)
                continue

            standard_initial_time = phone_bill_call.call_start.replace(
                hour=standard_initial_hours, minute=standard_initial_minutes
            )
            standard_final_time = phone_bill_call.call_start.replace(
                hour=standard_final_hours, minute=standard_final_minutes
            )
            reduced_final_time = phone_bill_call.call_start.replace(
                hour=reduced_final_hours, minute=reduced_final_minutes
            )

            if standard_initial_time <= phone_bill_call.call_start <= standard_final_time:
                phone_bill_call.price = constants.STANDARD_STANDING_CHARGE
                standard_time = True
            else:
                phone_bill_call.price = constants.REDUCED_STANDING_CHARGE
                standard_time = False

            if phone_bill_call.call_start > standard_initial_time:
                reduced_final_time = reduced_final_time + timedelta(days=1)

            aux_date = phone_bill_call.call_start
            while aux_date < phone_bill_call.call_end:
                if standard_time:
                    if phone_bill_call.call_end > standard_final_time:
                        comparsion_date = standard_final_time
                    else:
                        comparsion_date = phone_bill_call.call_end
                else:
                    if phone_bill_call.call_end > reduced_final_time:
                        comparsion_date = reduced_final_time
                    else:
                        comparsion_date = phone_bill_call.call_end
                    reduced_final_time = reduced_final_time + timedelta(days=1)

                minutes = (comparsion_date - aux_date).seconds // 60
                if standard_time:
                    phone_bill_call.price += minutes * constants.STANDARD_MINUTE_CHARGE
                else:
                    phone_bill_call.price += minutes * constants.REDUCED_MINUTE_CHARGE

                aux_date = comparsion_date
                standard_time = not standard_time

            self.total += phone_bill_call.price
            self.record_calls.append(phone_bill_call)

    def save(self):
        """Save the Phone Bill data on the database."""
        db = get_db()
        cursor = db.cursor()

        existent_period = self.exists_period()
        result = None
        if existent_period:
            self.id = existent_period
        else:
            fields = ['phone_number', 'period']

            sql_command = 'INSERT INTO {} ({}) VALUES ({})'.format(
                self.TABLE_NAME,
                ', '.join(fields),
                ', '.join(['?'] * len(fields))
            )
            values = [self.phone_number, self.period]
            result = cursor.execute(sql_command, values)

        if result and result.rowcount <= 0:
            return False
        elif result:
            self.id = result.lastrowid

        for call in self.record_calls:
            call.bill_id = self.id
            call.save()

        db.commit()

        return True


class PhoneBillCall:
    """Model to store phone bills calls."""

    TABLE_NAME = 'phone_bill_call'

    def __init__(self, destination_number, call_identifier, call_start, call_end, bill_id=None, bill_call_id=None):
        """Constructor used to populate the data of the object."""
        if call_identifier:
            existent = get_by_id(
                self.TABLE_NAME,
                'call_identifier',
                call_identifier,
                ['id', 'destination_number', 'call_start', 'call_end', 'duration', 'price']
            )
            if existent:
                self.call_identifier = call_identifier
                self.id = existent.get('id')
                self.destination_number = existent.get('destination_number')
                self.call_start = existent.get('call_start')
                self.call_end = existent.get('call_end')
                self.duration = existent.get('duration')
                self.bill_id = existent.get('bill_id')
                self.price = existent.get('price')
                return

        self.destination_number = destination_number
        self.call_identifier = call_identifier
        self.call_start = get_date_or_none(call_start)
        self.call_end = get_date_or_none(call_end)
        if self.call_start and self.call_end:
            self.duration = str(self.call_end - self.call_start)
        self.bill_id = bill_id
        self.price = None
        self.id = bill_call_id

    def to_dict(self):
        """Format the object in a json document."""
        return {
            'id': self.id,
            'destination_number': self.destination_number,
            'bill_id': self.bill_id,
            'call_identifier': self.call_identifier,
            'call_start': self.call_start,
            'call_end': self.call_end,
            'duration': self.duration,
            'price': self.price,
        }

    def validate(self):
        """
        Validate if the mandatory fields are present and are valid.

        Returns:
            (list): list of error messages generated by the validation.
        """
        error_messages = []

        if not self.destination_number:
            error_messages.append(constants.MESSAGE_MANDATORY_FIELD.format('destination_number'))
        elif not is_valid_phone_number(self.destination_number):
            error_messages.append(constants.MESSAGE_INVALID_FIELD.format('destination_number'))

        if not self.call_start:
            error_messages.append(constants.MESSAGE_MANDATORY_FIELD.format('call_start'))

        if not self.call_end:
            error_messages.append(constants.MESSAGE_MANDATORY_FIELD.format('call_end'))

        return error_messages

    def save(self):
        """Save the Call Record data on the database."""
        db = get_db()
        cursor = db.cursor()

        exists_id = check_exists_id(cursor, self.TABLE_NAME, 'id', self.id)

        if exists_id:
            update = (
                'destination_number = ?, call_start = ?, call_end = ?, duration = ?,'
                ' price = ?, call_identifier = ?, bill_id = ?'
            )

            sql_command = 'UPDATE {} SET {} WHERE id = ?'.format(self.TABLE_NAME, update)
        else:
            fields = [
                'destination_number', 'call_start', 'call_end', 'duration',
                'price', 'call_identifier', 'bill_id'
            ]
            if self.id:
                fields.append('id')

            sql_command = 'INSERT INTO {} ({}) VALUES ({})'.format(
                self.TABLE_NAME,
                ', '.join(fields),
                ', '.join(['?'] * len(fields))
            )

        values = [
            self.destination_number, self.call_start, self.call_end, self.duration,
            self.price, self.call_identifier, self.bill_id]
        if self.id:
            values.append(self.id)

        res = cursor.execute(sql_command, values)
        db.commit()

        return res.rowcount > 0


def check_exists_id(cursor, table_name, id_field, id_value):
    """
    Check if there is some record on the table with the id.

    Args:
        cursor (): Cursor object from sqlite.
        table_name (str): Name of the table that will be used in the verification.
        if_field (str): Name of the id field that will be used to check the value.
        id_value (int): Value of the id that will be searched on the id field of the table.

    Returns:
        True - id exists.
        False - id not exists.
    """
    if not id_value:
        return False

    sql_command = 'SELECT 1 FROM {} WHERE {} = {}'.format(table_name, id_field, id_value)
    result = cursor.execute(sql_command)

    return result.fetchone() is not None


def get_by_id(table_name, id_field, id_value, fields=None):
    """
    Check if there is some record on the table with the id.

    Args:
        table_name (str): Name of the table that will be used in the verification.
        if_field (str): Name of the id field that will be used to check the value.
        id_value (int): Value of the id that will be searched on the id field of the table.

    Returns:
        True - id exists.
        False - id not exists.
    """
    if not id_value:
        return None

    cursor = get_db().cursor()

    sql_command = 'SELECT {} FROM {} WHERE {} = {}'.format(
        '*' if not fields else ', '.join(fields),
        table_name,
        id_field,
        id_value
    )
    result = cursor.execute(sql_command).fetchone()

    if result:
        return dict(result)

    return None
