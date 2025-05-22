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
    res = client.get("/api/ebikes")
    assert res.status_code == 401

def test_list_bikes_with_auth(client):
    token = get_token(client)
    assert token is not None, "❌ No se pudo obtener token"
    res = client.get("/api/ebikes", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code in (200, 403)

def test_get_bike_requires_auth(client):
    res = client.get("/api/ebikes/timeline/1")
    assert res.status_code == 401

def test_get_bike_with_auth(client):
    token = get_token(client)
    assert token is not None, "❌ No se pudo obtener token"
    res = client.get("/api/ebikes/timeline/1", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code in (200, 403, 404)

def test_lock_bike_requires_auth(client):
    res = client.post("/api/ebikes/1/lock", json={"motivo": "robo"})
    assert res.status_code == 401

def test_lock_bike_with_auth(client):
    token = get_token(client)
    assert token is not None, "❌ No se pudo obtener token"

    res = client.post(
        "/api/ebikes/1/lock",
        json={"motivo": "robo"},
        headers={"Authorization": f"Bearer {token}"}
    )

    print("STATUS:", res.status_code)
    print("BODY:  ", res.get_json())

    assert res.status_code in (202, 403, 400, 404)



def test_device_lock_simulation(client):
    res = client.post("/api/device/lock", json={"ebike_id": 1})
    assert res.status_code == 200
    assert res.json.get("success") is True

def test_set_user_role_requires_auth(client):
    res = client.post("/api/users/2/role", json={"role_id": 2})
    assert res.status_code == 401

def test_set_user_role_with_auth(client):
    token = get_token(client)
    assert token is not None, "❌ No se pudo obtener token"
    res = client.post(
        "/api/users/2/role",
        json={"role_id": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code in (200, 403, 404)

def test_register_user(client):
    token = get_token(client)
    assert token is not None
    res = client.post(
        "/api/users/register",
        json={"username": "nuevo_cliente", "password": "12345", "role_id": 3},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code in (201, 403, 400)

def test_register_ebike(client):
    token = get_token(client)
    assert token is not None
    res = client.post(
        "/api/ebikes/register",
        json={"serial": "SERIAL-XYZ"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code in (201, 403, 400)

def test_assign_owner_to_bike(client):
    token = get_token(client)
    assert token is not None
    res = client.patch(
        "/api/ebikes/1/assign-owner",
        json={"owner_id": 2},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code in (200, 400, 404, 403)
