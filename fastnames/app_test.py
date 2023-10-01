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
    """Test home page availability."""
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_add_nicknames_get(client: TestClient) -> None:
    """Test add_nicknames page availability."""
    response = client.get('/add/')
    assert response.status_code == HTTPStatus.OK
