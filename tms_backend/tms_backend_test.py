from .settings import mongo


def test_home_api(client):
    response = client.get('/')
    data = {'name': 'Transaction management system(Backend)',
            'description': 'This is a backend for a transaction management system'}
    assert response.is_json is True
    assert response.json == data


def test_testdata_function(client, monkeypatch):
    class MockDbObject:
        class testCollection:
            def find(self):
                return {'value': 'hello'}

    monkeypatch.setattr(mongo, 'db', MockDbObject)

    response = client.get('/testdata')
    assert b'the dummy data is  value' == response.data
