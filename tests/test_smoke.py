"""TD-01 smoke tests."""


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Moffat Bay Lodge" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"service": "moffat-bay", "status": "ok"}
