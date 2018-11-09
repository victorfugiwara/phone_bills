"""API for olist technical test."""
from flask import Blueprint, jsonify, render_template, request

from api import constants
from api.models import CallRecord


blueprint = Blueprint('api', __name__, url_prefix='/')


@blueprint.route('/', methods=['GET'])
def home():
    """Home endpoint that shows the description of the project."""
    return render_template('index.html')


@blueprint.route('/api/v1/phone_call', methods=['POST'])
def phone_call():
    """Endpoint to receive the telephone calls records and save it on the database."""
    data = request.json
    if data:
        record = CallRecord(
            data.get('id'),
            data.get('type'),
            data.get('timestamp'),
            data.get('call_id'),
            data.get('source'),
            data.get('destination'),
        )
        errors = record.validate()
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            })

        if record.save():
            return jsonify({
                'success': True,
                'record_id': record.record_id
            })

    return jsonify({
        'success': False,
        'errors': constants.MESSAGE_INVALID_DATA_REQUEST
    })


@blueprint.route('/api/v1/phone_bill', methods=['GET'])
def phone_bill():
    """Endpoint to return the telephone bills."""
    data = request.json
    return jsonify([data])
