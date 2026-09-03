"""TD-01 smoke tests."""


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Moffat Bay Lodge" in response.data
    assert b"/static/images/hero-moffat-bay.jpg" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"service": "moffat-bay", "status": "ok"}


def test_required_public_pages_load(client):
    for route, required_copy in [
        ("/about", b"A slower way to meet the island."),
        ("/contact", b"We are here to help plan your island stay."),
        ("/attractions", b"Hiking"),
    ]:
        response = client.get(route)

        assert response.status_code == 200
        assert required_copy in response.data

    attractions_response = client.get("/attractions")
    for activity in (b"Hiking", b"Kayaking", b"Whale watching", b"Scuba diving"):
        assert activity in attractions_response.data
