from flask import Flask, jsonify, json
from .transactions.transactions import transactions
from .settings import mongo
from flask.cli import AppGroup

from constants import *

tms_backend = Flask(__name__)

db = AppGroup('db')


tms_backend.register_blueprint(transactions)

tms_backend.config.from_object('config')

mongo.init_app(tms_backend)

@tms_backend.route('/')
def home_api():
    return jsonify(name='Transaction management system(Backend)',
                   description='This is a backend for a transaction management system')


@tms_backend.route('/testdata')
def test_route():
    data = mongo.db.testCollection.find({})
    for value in data:
        print(value)
    return 'the dummy data is  %s' % value


@db.command('run')
def run_migrations():
    try:
        mongo.db.create_collection(transactions_collection)
    except Exception as e:
        print(e, ', so skipping creation')


@db.command('import_dummy_data')
def import_dummy_data():
    with open('testData/dummydata.json') as f:
        json_data = json.load(f)
        print("deleting old records")
        mongo.db[transactions_collection].delete_many({})
        result = mongo.db[transactions_collection].insert_many(json_data['transactions'])


tms_backend.cli.add_command(db)
