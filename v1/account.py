from flask import Blueprint, request, jsonify

from database import Session
from models import Account
import hashlib

account_blueprint = Blueprint('account_blueprint', __name__)


@account_blueprint.route('/v1/account/by-id', methods=['POST'])
def get_account_by_id():
    req = request
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
    password = hashlib.sha256(request.json['password'].encode()).hexdigest()
    session = Session()
    account = session.query(Account).filter_by(username=username, password=password).first()
    if account is not None:
        account = account.to_dict()
    session.close()
    return jsonify(account)

@account_blueprint.route('/v1/account/create', methods=['POST'])
def create_account():
    username = request.json.get('username')
    email = request.json['email']
    password = hashlib.sha256(request.json['password'].encode()).hexdigest()
    orders = []
    session = Session()
    # First check if the account exists
    account = session.query(Account).filter_by(email=email, username=username).first()
    if account is None:
        # Account does not exist - create it.
        account = Account(username=username, email=email, password=password, orders=orders)
        session.add(account)
        session.commit()
        account = account.to_dict()
        session.close()
        return jsonify(account)
    else:
        # Account does exist - send them nothing.
        session.close()
        return jsonify(None)

@account_blueprint.route('/v1/account/change-password', methods=['POST'])
def change_password():
    account_id = int(request.json['id'])
    password = hashlib.sha256(request.json['password'].encode()).hexdigest()
    session = Session()
    account = session.query(Account).filter_by(id=account_id).first()
    account.password = password
    session.commit()
    session.close()
    return jsonify(True)

@account_blueprint.route('/v1/account/update-email', methods=['POST'])
def update_email():
    account_id = int(request.json['id'])
    email = request.json['email']
    session = Session()
    account = session.query(Account).filter_by(id=account_id).first()
    account.email = email
    session.commit()
    session.close()
    return jsonify(True)
