"""Main app test."""
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    """App startup."""
    from fastnames.main import app

    yield TestClient(app)


def test_home_get(client: TestClient) -> None:
    """Test home route."""
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_add_nicknames_get(client: TestClient) -> None:
    """Test /add/ route."""
    response = client.get('/add/')
    assert response.status_code == HTTPStatus.OK


def test_get_names(client: TestClient) -> None:
    """Test /get-names/ route."""
    response = client.get('/get-names/')
    assert response.status_code == HTTPStatus.OK
