from flask import Blueprint, request, jsonify
from sqlalchemy import asc

from database import Session
from models import Option
from v1.default_options import OptionType

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
        if o['type'] is OptionType.TOGGLE:
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
