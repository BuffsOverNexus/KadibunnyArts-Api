from flask import Blueprint, request, jsonify
from sqlalchemy import asc

from database import Session
from models import Option

option_blueprint = Blueprint('option_blueprint', __name__)


@option_blueprint.route('/v1/options', methods=['POST', 'GET'])
def get_all_options():
    session = Session()
    options = session.query(Option).order_by(asc(Option.id)).all()
    options = [option.to_dict() for option in options]
    session.close()
    return jsonify(options)


@option_blueprint.route('/v1/option/by-id', methods=['POST'])
def get_option_by_id():
    option_id = int(request.json['id'])
    session = Session()
    option = session.query(Option).filter_by(id=option_id).first()
    if option is not None:
        option = option.to_dict()
    session.close()
    return jsonify(option)


@option_blueprint.route('/v1/option/save', methods=['POST'])
def save_option():
    option_id = int(request.json['id'])
    key = request.json['key']
    value = request.json['value']
    session = Session()
    option = session.query(Option).filter_by(id=option_id).first()
    option.key = key
    option.value = value
    session.commit()
    session.close()
    return jsonify(True)

@option_blueprint.route('/v1/option/save/all', methods=['POST'])
def save_all_options():
    options = request.json['options']
    session = Session()
    for o in options:
        session.begin()
        option = session.query(Option).filter_by(id=o['id']).first()
        if o['type'] is 0:
            option.value = str(o['value']).lower()
        else:
            option.value = str(o['value'])
        session.commit()

    session.commit()
    options = session.query(Option).order_by(asc(Option.id)).all()
    options = [option.to_dict() for option in options]
    session.close()
    return jsonify(options)


@option_blueprint.route('/v1/option/by-key', methods=['POST'])
def get_option_by_key():
    key = request.json['key']
    session = Session()
    option = session.query(Option).filter_by(key=key).first()
    if option is not None:
        option = option.to_dict()
    session.close()
    return jsonify(option)

# The website should have default keys that are automatically used.
def create_default_keys():
    session = Session()
    has_commission_status = session.query(Option).filter_by(key="COMMISSION_STATUS").first() is not None
    has_disabled_message = session.query(Option).filter_by(key="COMMISSION_DISABLED_MESSAGE").first() is not None

    option_commission_available = Option()
    option_commission_disabled_message = Option()
    option_commission_available.key = "COMMISSION_STATUS"
    option_commission_available.value = "false"
    option_commission_available.type = 0
    option_commission_available.title = "Commission Form Availability"
    option_commission_available.description = "Allow new commission requests?"

    option_commission_disabled_message.key = "COMMISSION_DISABLED_MESSAGE"
    option_commission_disabled_message.value = "New commission requests are currently unavailable. Please try again later."
    option_commission_disabled_message.type = 2 # Text Area
    option_commission_disabled_message.title = "Commissions Unavailable Message"
    option_commission_disabled_message.description = "Please enter in what the user will see when visiting the Commissions form when it is not available:"

    if not has_commission_status:
        session.add(option_commission_available)
    if not has_disabled_message:
        session.add(option_commission_disabled_message)
    session.commit()
    session.close()