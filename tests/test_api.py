"""Tests for api.py file."""
import mock

from api import api


PHONE_CALL_ENDPOINT = '/api/v1/phone_call'
PHONE_BILL_ENDPOINT = '/api/v1/phone_bill'


@mock.patch('api.api.render_template')
def test_home(render_template):
    """Test home function."""
    api.home()
    render_template.assert_called_once_with('index.html')


def test_phone_call_without_data(client):
    """Test phone_call function when there is no data on the request."""
    result = client.post(PHONE_CALL_ENDPOINT)

    assert not result.json.get('success')
    assert result.json.get('errors') == 'Invalid data request.'


@mock.patch('api.api.CallRecord')
def test_phone_call_error_validate(record_class, client):
    """Test phone_call function when there is error on validation of the record."""
    data = [{'type': 'xxx', 'timestamp': 'invalid', 'call_id': 10, 'source': '321', 'destination': '123'}]
    record_class.return_value.validate.return_value = ['invalid data']
    result = client.post(PHONE_CALL_ENDPOINT, json=data)

    assert not result.json.get('success')
    assert 'invalid data' in result.json.get('errors')

    record_class.assert_called_once_with(
        data[0].get('id'),
        data[0].get('type'),
        data[0].get('timestamp'),
        data[0].get('call_id'),
        data[0].get('source'),
        data[0].get('destination')
    )


@mock.patch('api.api.CallRecord')
def test_phone_call_not_saving(record_class, client):
    """Test phone_call function when the save method returns False."""
    data = [
        {'type': 'start', 'timestamp': '2018-11-10T12:22:14', 'call_id': 10, 'source': '321', 'destination': '123'},
        {'type': 'end', 'timestamp': '2018-11-10T12:25:32', 'call_id': 10},
    ]
    record_class.return_value.validate.return_value = []
    record_class.return_value.save.return_value = False
    result = client.post(PHONE_CALL_ENDPOINT, json=data)

    assert not result.json.get('success')
    assert result.json.get('errors') == 'Invalid data request.'

    assert_calls = []
    for item in data:
        assert_calls.append(
            mock.call(
                item.get('id'),
                item.get('type'),
                item.get('timestamp'),
                item.get('call_id'),
                item.get('source'),
                item.get('destination')
            )
        )
        assert_calls.append(mock.call().validate())
        assert_calls.append(mock.call().save())
    record_class.assert_has_calls(assert_calls)


@mock.patch('api.api.CallRecord')
def test_phone_call_saved(record_class, client):
    """Test phone_call function when the records are save with success."""
    data = [
        {'type': 'start', 'timestamp': '2018-11-10T12:22:14', 'call_id': 10, 'source': '321', 'destination': '123'},
        {'type': 'end', 'timestamp': '2018-11-10T12:25:32', 'call_id': 10},
    ]
    record_class.return_value.validate.return_value = []
    record_class.return_value.save.return_value = True
    result = client.post(PHONE_CALL_ENDPOINT, json=data)

    assert result.json.get('success')
    assert result.json.get('processed') == 2

    assert_calls = []
    for item in data:
        assert_calls.append(
            mock.call(
                item.get('id'),
                item.get('type'),
                item.get('timestamp'),
                item.get('call_id'),
                item.get('source'),
                item.get('destination')
            )
        )
        assert_calls.append(mock.call().validate())
        assert_calls.append(mock.call().save())
    record_class.assert_has_calls(assert_calls)


def test_phone_bill_without_data(client):
    """Test phone_bill function when there is no data on the request."""
    result = client.get(PHONE_BILL_ENDPOINT)

    assert not result.json.get('success')
    assert result.json.get('errors') == 'Invalid data request.'


@mock.patch('api.api.PhoneBill')
def test_phone_bill_error_validate(record_class, client):
    """Test phone_bill function when there is error on validation of the record."""
    endpoint_args = 'subscriber=12345'
    record_class.return_value.validate.return_value = ['invalid data']
    result = client.get('{}?{}'.format(PHONE_BILL_ENDPOINT, endpoint_args))

    assert not result.json.get('success')
    assert 'invalid data' in result.json.get('errors')

    record_class.assert_called_once_with('12345', None)


@mock.patch('api.api.PhoneBill')
def test_phone_bill_not_saving(record_class, client):
    """Test phone_bill function when the save method returns False."""
    endpoint_args = 'subscriber=12345'
    record_class.return_value.validate.return_value = []
    record_class.return_value.save.return_value = False
    result = client.get('{}?{}'.format(PHONE_BILL_ENDPOINT, endpoint_args))

    assert not result.json.get('success')
    assert result.json.get('errors') == 'Invalid data request.'

    record_class.return_value.calculate_phone_bill.assert_called_once_with()
    record_class.assert_called_once_with('12345', None)


@mock.patch('api.api.PhoneBill')
def test_phone_bill_saved(record_class, client):
    """Test phone_bill function when the records are save with success."""
    endpoint_args = 'subscriber=12345&period=11/2018'
    record_class.return_value.validate.return_value = []
    record_class.return_value.save.return_value = True
    record_class.return_value.to_dict.return_value = {'dict': 'data'}
    result = client.get('{}?{}'.format(PHONE_BILL_ENDPOINT, endpoint_args))

    assert result.json.get('success')
    assert result.json.get('data') == {'dict': 'data'}

    record_class.return_value.calculate_phone_bill.assert_called_once_with()
    record_class.assert_called_once_with('12345', '11/2018')
