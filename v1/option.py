from flask import Blueprint, request, jsonify
from sqlalchemy import Date

from database import Session
from models import Account, Order, Option

option_blueprint = Blueprint('option_blueprint', __name__)

@option_blueprint.route('/v1/options')
def get_all_options():
    session = Session()
    options = session.query(Option).all()
    options = [option.to_dict() for option in options]
    session.close()
    return jsonify(options)


@option_blueprint.route('/v1/option/by-id')
def get_option_by_id():
    option_id = int(request.json['id'])
    session = Session()
    option = session.query(Option).filter_by(id=option_id).first()
    if option is not None:
        option = option.to_dict()
    session.close()
    return jsonify(option)


@option_blueprint.route('/v1/option/save')
def save_option():
    option_id = int(request.jsoni['id'])
    key = request.json['key']
    value = request.json['value']
    session = Session()
    option = session.query(Option).filter_by(id=option_id).first()
    option.key = key
    option.value = value
    session.commit()
    session.close()
    return jsonify(True)


@option_blueprint.route('/v1/option/by-key')
def get_option_by_key():
    key = request.json['key']
    session = Session()
    option = session.query(Option).filter_by(key=key).first()
    if option is not None:
        option = option.to_dict()
    session.close()
    return jsonify(option)