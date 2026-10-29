from fastapi.testclient import TestClient
from httpx import Response

from main import app

client: TestClient = TestClient(app)


def test_hello() -> None:
    response: Response = client.get("/hello")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello from Notes API"}


def test_create_and_get_note() -> None:
    user_payload: dict = {
        "username": "user1",
        "email" : "user1@example.com",
    }
    user_response: Response = client.post(
        "/users",
        json=user_payload,
    )
    assert user_response.status_code == 201
    user_id: int = user_response.json()["id"]

    note_payload: dict = {
        "title": "Integration Test Note",
        "content": "Testing create and get flow.",
        "status": "active",
        "user_id": user_id,
    }
    create_response: Response = client.post(
        "/notes",
        json=note_payload
    )
    assert create_response.status_code == 201
    created_data: dict = create_response.json()
    note_id: int = created_data["id"]

    get_response: Response = client.get(f"/notes/{note_id}")
    assert get_response.status_code == 200
    fetched_data: dict = get_response.json()

    assert fetched_data["id"] == note_id
    assert fetched_data["title"] == note_payload["title"]
    assert fetched_data["content"] == note_payload["content"]
    assert fetched_data["status"] == note_payload["status"]
    assert fetched_data["user_id"] == user_id
