from flask import Blueprint, request, jsonify
from sqlalchemy import Date

from database import Session
from models import Account, Order

order_blueprint = Blueprint('order_blueprint', __name__)

@order_blueprint.route('/v1/order/by-id', methods=['POST'])
def get_order_by_id():
    order_id = int(request.json['id'])
    session = Session()
    order = session.query(Order).filter_by(id=order_id).first()

    session.close()
    return jsonify(order)

@order_blueprint.route('/v1/order/create')
def create_order():
    # Gather all data from the submission
    session = Session()

    session.close()
    return jsonify(True)
