import pytest
from tms_backend.tms_backend import tms_backend


@pytest.fixture
def client():
    tms_backend.config['TESTING'] = True
    with tms_backend.test_client() as client:
        yield client
