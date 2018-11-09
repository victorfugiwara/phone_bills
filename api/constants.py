"""Constant values used by the api."""

RECORD_TYPE_START = 'start'
RECORD_TYPE_END = 'end'
RECORD_TYPE_OPTIONS = {
    RECORD_TYPE_START: 'Start call',
    RECORD_TYPE_END: 'End call',
}

MESSAGE_MANDATORY_FIELD = 'The field {} is mandatory.'
MESSAGE_INVALID_FIELD = 'The field {} has an invalid value.'
MESSAGE_DUPLICATED_CALL_ID = 'Database already has a record with given call id {} record type {} with other record id.'

MESSAGE_INVALID_DATA_REQUEST = 'Invalid data request.'
