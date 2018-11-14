"""API for olist technical test."""
from flask import Blueprint, jsonify, render_template, request

from api import constants
from api.models import CallRecord, PhoneBill


blueprint = Blueprint('api', __name__, url_prefix='/')


@blueprint.route('/', methods=['GET'])
def home():
    """Home endpoint that shows the description of the project."""
    return render_template('index.html')


@blueprint.route('/api/v1/phone_call', methods=['POST'])
def phone_call():
    """Endpoint to receive the telephone calls records and save it on the database."""
    data = request.json
    if not data:
        return jsonify({
            'success': False,
            'errors': constants.MESSAGE_INVALID_DATA_REQUEST
        })

    all_records = []
    for item in data:
        record = CallRecord(
            item.get('id'),
            item.get('type'),
            item.get('timestamp'),
            item.get('call_id'),
            item.get('source'),
            item.get('destination'),
        )

        errors = record.validate()
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            })

        if record.save():
            all_records.append(record)

    if all_records:
        return jsonify({
            'success': True,
            'processed': len(all_records)
        })

    return jsonify({
        'success': False,
        'errors': constants.MESSAGE_INVALID_DATA_REQUEST
    })


@blueprint.route('/api/v1/phone_bill', methods=['GET'])
def phone_bill():
    """Endpoint to return the telephone bills."""
    data = request.args
    if not data:
        return jsonify({
            'success': False,
            'errors': constants.MESSAGE_INVALID_DATA_REQUEST
        })

    phone_bill = PhoneBill(data.get('subscriber'), data.get('period'))
    errors = phone_bill.validate()
    if errors:
        return jsonify({
            'success': False,
            'errors': errors
        })

    phone_bill.calculate_phone_bill()
    if phone_bill.save():
        return jsonify({
            'success': True,
            'data': phone_bill.to_dict()
        })

    return jsonify({
        'success': False,
        'errors': constants.MESSAGE_INVALID_DATA_REQUEST
    })
