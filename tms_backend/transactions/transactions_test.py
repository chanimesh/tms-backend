from ..settings import mongo
from flask import jsonify


def test_transactions_returned_when_requested(client, monkeypatch):
    transaction_data = [
        {
            "transaction_id": 1,
            "type": "CREDIT",
            "date": "22-10-2019",
            "amount": 22.85
        },
        {
            "transaction_id": 2,
            "type": "DEBIT",
            "date": "22-10-2019",
            "amount": 22.85
        },
        {
            "transaction_id": 3,
            "type": "CREDIT",
            "date": "25-10-2019",
            "amount": 2343
        },
        {
            "transaction_id": 1,
            "type": "CREDIT",
            "date": "22-10-2029",
            "amount": 223
        },

    ]

    class MockDbObject:
        def __getitem__(self, key):
            return getattr(self, key)

        class transactions:
            def find(self, data):
                return transaction_data

    mongo_mock = MockDbObject()

    monkeypatch.setattr(mongo, 'db', mongo_mock)
    response = client.get('/transactions/')
    response_data = jsonify({"transactions": transaction_data})
    assert response.data == response_data.data
