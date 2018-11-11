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

MESSAGE_INVALID_PERIOD = 'The field period must be a closed period.'

MESSAGE_INVALID_DATA_REQUEST = 'Invalid data request.'
MESSAGE_ERROR_SAVE = 'An error occurred. Please, try again or contact the support team.'

STANDARD_INITIAL_TIME = '06:00'
STANDARD_FINAL_TIME = '21:59'
STANDARD_STANDING_CHARGE = 0.36
STANDARD_MINUTE_CHARGE = 0.09

REDUCED_INITIAL_TIME = '22:00'
REDUCED_FINAL_TIME = '05:59'
REDUCED_STANDING_CHARGE = 0.36
REDUCED_MINUTE_CHARGE = 0.0
