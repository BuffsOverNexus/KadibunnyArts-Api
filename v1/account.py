from flask import Blueprint, request, jsonify

from database import Session
from models import Account

account_blueprint = Blueprint('account_blueprint', __name__)

@account_blueprint.route('/v1/account/by-id', methods=['POST'])
def get_account_by_id():
    account_id = int(request.json['id'])
    session = Session()
    account = session.query(Account).filter_by(id=account_id).first()
    if account is not None:
        account = account.to_dict()
    session.close()
    return jsonify(account)

@account_blueprint.route('/v1/account/by-login', methods=['POST'])
def get_account_by_login():
    username = request.json['username']
    password = request.json['password']
    session = Session()
    account = session.query(Account).filter_by(username=username, password=password).first()
    if account is not None:
        account = account.to_dict()
    session.close()
    return jsonify(account)

@account_blueprint.route('/v1/account/create', methods=['POST'])
def create_account():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    orders = []
    session = Session()
    # First check if the account exists
    account = session.query(Account).filter_by(email=email, username=username).first()
    if account is None:
        account = Account(username=username, email=email, password=password, orders=orders)
        session.add(account)
        session.commit()
        account = account.to_dict()
        return jsonify(account)
    else:
        return jsonify(None)
