import sys

import flask.templating
from flask import Flask, jsonify
from flask_cors import CORS

from database import Base, postgres_engine
from v1.account import account_blueprint
from v1.option import option_blueprint, create_default_keys
from v1.order import order_blueprint

app = Flask(__name__)

# Add local-only CORS exception.
# Potentially may need to remove this in the future.
CORS(app)

app.register_blueprint(account_blueprint)
app.register_blueprint(order_blueprint)
app.register_blueprint(option_blueprint)

# Create schema
Base.metadata.create_all(postgres_engine)

# Add default keys
create_default_keys()