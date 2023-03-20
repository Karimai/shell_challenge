import http
import json

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == http.HTTPStatus.OK
    assert response.json() == {"message": "test"}


def test_get_weather():
    response = client.get(
        "/weather/",
        params={
            "latitude": 40.7128,
            "longitude": -74.0060,
        },
    )
    assert response.status_code == http.HTTPStatus.OK
    response = json.loads(response.text)
    assert len(eval(response)) == 16

    response = client.get(
        "/weather/",
        params={
            "latitude": 28014,
        },
    )

    assert response.status_code == http.HTTPStatus.OK
    response = json.loads(response.text)
    assert len(eval(response)) == 16

    response = client.get(
        "/weather/",
        params={
            "latitude": "WrongData",
        },
    )

    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
