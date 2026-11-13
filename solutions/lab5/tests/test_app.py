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


def test_valid_login_still_works(client):
    response = client.post("/login", data={
        "username": "student",
        "password": "student123",
    })
    assert response.status_code == 302


def test_login_sql_injection_is_blocked(client):
    response = client.post("/login", data={
        "username": "admin' -- ",
        "password": "wrong",
    })
    assert response.status_code == 200
    assert "Неверные учётные данные" in response.get_data(as_text=True)


def test_search_treats_quote_as_text(client):
    response = client.get("/search?q=' OR '1'='1")
    assert response.status_code == 200
    assert "Правило лаборатории" not in response.get_data(as_text=True)


def login(client, username, password):
    return client.post("/login", data={"username": username, "password": password})


def test_profile_requires_login(client):
    assert client.get("/profile?id=1").status_code == 401


def test_student_cannot_read_foreign_profile(client):
    login(client, "student", "student123")
    assert client.get("/profile?id=1").status_code == 403


def test_student_reads_own_profile(client):
    login(client, "student", "student123")
    response = client.get("/profile?id=2")
    assert response.status_code == 200
    assert "student@example.test" in response.get_data(as_text=True)


def test_admin_reads_any_profile(client):
    login(client, "admin", "admin123")
    assert client.get("/profile?id=3").status_code == 200


def test_security_headers_are_set(client):
    headers = client.get("/").headers
    assert "default-src 'self'" in headers["Content-Security-Policy"]
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"


def test_stored_content_is_escaped(client):
    client.post("/comments", data={
        "author": "student",
        "content": "<b>training-xss</b>",
    })
    page = client.get("/comments").get_data(as_text=True)
    assert "<b>training-xss</b>" not in page
    assert "&lt;b&gt;training-xss&lt;/b&gt;" in page


def test_search_query_is_escaped(client):
    page = client.get("/search?q=<b>x</b>").get_data(as_text=True)
    assert "<b>x</b>" not in page
