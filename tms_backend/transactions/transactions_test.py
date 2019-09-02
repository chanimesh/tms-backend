from ..settings import mongo
import json
import mongomock
import pytest
import copy

from constants import *

@pytest.fixture
def dummy_data():
    with open('testData/dummydata.json') as f:
        dummy_data = json.load(f)
    return dummy_data


def test_transactions_returned_when_requested(client, dummy_data, monkeypatch):

    class MockDbObject:
        def __getitem__(self, key):
            return getattr(self, key)

        class transactions:
            def find(self, data):
                return dummy_data['transactions']

    mongo_mock = MockDbObject()

    monkeypatch.setattr(mongo, 'db', mongo_mock)
    response = client.get('/transactions/')
    assert response.json == dummy_data


def test_transactions_returned_when_requested_with_mongomock(client, dummy_data, monkeypatch):

    mongo_db = mongomock.MongoClient().db
    data = copy.deepcopy(dummy_data)
    mongo_db[transactions_collection].insert_many(data['transactions'])
    monkeypatch.setattr(mongo, 'db', mongo_db)
    response = client.get('/transactions/')
    assert response.json == dummy_data
