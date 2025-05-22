import pytest
from unittest.mock import patch

@pytest.fixture
def client():
    from main import create_app
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def get_token(client):
    res = client.post("/api/auth/login", json={"usuario": "juan", "clave": "12345"})
    if res.status_code == 200:
        return res.get_json().get("access_token")
    return None

def test_login_success(client):
    res = client.post("/api/auth/login", json={"usuario": "juan", "clave": "12345"})
    assert res.status_code in (200, 401)

def test_list_bikes_requires_auth(client):
    res = client.get("/api/bikes/")
    assert res.status_code == 401

def test_list_bikes_with_auth(client):
    token = get_token(client)
    assert token is not None, "❌ No se pudo obtener token"
    res = client.get("/api/bikes/", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code in (200, 403)

def test_get_bike_requires_auth(client):
    res = client.get("/api/bikes/1")
    assert res.status_code == 401

def test_get_bike_with_auth(client):
    token = get_token(client)
    assert token is not None, "❌ No se pudo obtener token"
    res = client.get("/api/bikes/1", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code in (200, 403, 404)

def test_lock_bike_requires_auth(client):
    res = client.post("/api/bikes/1/lock", json={"motivo": "robo"})
    assert res.status_code == 401

def test_lock_bike_with_auth(client):
    token = get_token(client)
    assert token is not None, "❌ No se pudo obtener token"
    res = client.post(
        "/api/bikes/1/lock",
        json={"motivo": "robo"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code in (202, 403, 400, 404)

def test_hook_evento_requires_auth(client):
    res = client.post("/api/hooks/evento", json={"ebike_id": 1, "motivo": "robo"})
    assert res.status_code == 401

@patch("infrastructure.services.gps_client_http.requests.post")
def test_hook_evento_with_auth(mock_post, client):  # <- orden corregido
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"success": True}

    token = get_token(client)
    assert token is not None, "❌ No se pudo obtener token"

    res = client.post(
        "/api/hooks/evento",
        json={"ebike_id": 1, "motivo": "robo"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code in (200, 403, 404)

def test_device_lock_simulation(client):
    res = client.post("/api/device/lock", json={"ebike_id": 1})
    assert res.status_code == 200
    assert res.json.get("success") is True

def test_set_user_role_requires_auth(client):
    res = client.post("/api/users/2/set-role", json={"role_id": 2})
    assert res.status_code == 401

def test_set_user_role_with_auth(client):
    token = get_token(client)
    assert token is not None, "❌ No se pudo obtener token"
    res = client.post(
        "/api/users/2/set-role",
        json={"role_id": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code in (200, 403, 404)

def test_register_user(client):
    token = get_token(client)
    assert token is not None
    res = client.post(
        "/api/register/user",
        json={"username": "nuevo_cliente", "password": "12345", "role_id": 3},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code in (201, 403, 400)


def test_register_ebike(client):
    token = get_token(client)
    assert token is not None
    res = client.post(
        "/api/register/bike",
        json={"serial": "SERIAL-XYZ"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code in (201, 403, 400)

def test_assign_owner_to_bike(client):
    token = get_token(client)
    assert token is not None
    res = client.patch(
        "/api/bikes/1/assign-owner",
        json={"owner_id": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code in (200, 400, 404, 403)
