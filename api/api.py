"""API for olist technical test."""
from flask import Blueprint, jsonify, render_template


blueprint = Blueprint('api', __name__, url_prefix='/')


@blueprint.route('/', methods=['GET'])
def home():
    """Home endpoint that shows the description of the project."""
    return render_template('index.html')


@blueprint.route('/api/v1/phone_call', methods=['POST'])
def phone_call():
    """Endpoint to receive the telephone calls records and save it on the database."""
    return jsonify([])


@blueprint.route('/api/v1/phone_bill', methods=['GET'])
def phone_bill():
    """Endpoint to return the telephone bills."""
    return jsonify([])
