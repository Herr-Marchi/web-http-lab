from fastapi.testclient import TestClient
from httpx import Response

from main import app

client: TestClient = TestClient(app)


def test_hello() -> None:
    response: Response = client.get("/hello")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello from Notes API"}
