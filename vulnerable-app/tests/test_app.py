import pytest

from backend.app import create_app


@pytest.fixture()
def client(tmp_path):
    app = create_app({
        "TESTING": True,
        "DATABASE_PATH": str(tmp_path / "test.db"),
    })
    return app.test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_login_sql_injection_is_demonstrable(client):
    response = client.post("/login", data={
        "username": "admin' -- ",
        "password": "wrong",
    })
    assert response.status_code == 302


def test_profile_is_available_without_authentication(client):
    response = client.get("/profile?id=1")
    assert response.status_code == 200
    assert "admin@example.test" in response.get_data(as_text=True)


def test_stored_content_is_rendered_without_escaping(client):
    client.post("/comments", data={
        "author": "student",
        "content": "<b>training-xss</b>",
    })
    response = client.get("/comments")
    assert "<b>training-xss</b>" in response.get_data(as_text=True)
