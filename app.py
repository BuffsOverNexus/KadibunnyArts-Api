import sys

from flask import Flask, jsonify
from flask_cors import CORS

from database import Base, postgres_engine
from v1.account import account_blueprint
from v1.option import option_blueprint
from v1.order import order_blueprint

app = Flask(__name__)

# Add local-only CORS exception
if sys.argv[0] is "LOCAL":
    CORS(app)

app.register_blueprint(account_blueprint)
app.register_blueprint(order_blueprint)
app.register_blueprint(option_blueprint)

Base.metadata.create_all(postgres_engine)


@app.route('/version')
def hello_world():
    return jsonify('0.5')


if __name__ == '__main__':
    app.run()
