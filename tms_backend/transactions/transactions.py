from flask import Blueprint, jsonify

from ..settings import mongo

from constants import *

transactions = Blueprint('transactions', 'transactions', url_prefix='/transactions')


@transactions.route('/')
def get_transactions():
    transactions_data = mongo.db[transactions_collection].find({}, {"_id": False})
    transactions_list = list(transactions_data)
    return jsonify({'transactions': transactions_list})
