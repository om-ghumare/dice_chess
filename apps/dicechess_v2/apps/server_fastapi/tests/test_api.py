from fastapi.testclient import TestClient

from app.main import app


def _auth_headers(client: TestClient) -> dict[str, str]:
    res = client.post("/auth/guest")
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_guest_auth():
    client = TestClient(app)
    res = client.post("/auth/guest")
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert "user_id" in body


def test_profile_me():
    client = TestClient(app)
    headers = _auth_headers(client)
    res = client.get("/profile/me", headers=headers)
    assert res.status_code == 200
    assert "display_name" in res.json()


def test_room_create_and_join():
    client = TestClient(app)
    headers_a = _auth_headers(client)
    headers_b = _auth_headers(client)
    created = client.post("/rooms", headers=headers_a).json()
    code = created["room_code"]
    joined = client.post(f"/rooms/{code}/join", headers=headers_b)
    assert joined.status_code == 200
    assert len(joined.json()["players"]) == 2


def test_matchmaking_pairing():
    client = TestClient(app)
    headers_a = _auth_headers(client)
    headers_b = _auth_headers(client)
    a = client.post("/matchmaking/enqueue", headers=headers_a, json={"queue": "casual"}).json()
    b = client.post("/matchmaking/enqueue", headers=headers_b, json={"queue": "casual"}).json()
    assert a["matched"] is False
    assert b["matched"] is True
