"""TD-01 smoke tests."""


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Moffat Bay Lodge" in response.data
    assert b'href="/attractions"' in response.data
    assert b"Explore attractions" in response.data
    assert b"/static/images/hero-moffat-bay.jpg" in response.data
    assert b"/static/images/SalishSalmonv2.png" in response.data
    assert b"Salish salmon artwork in black on a transparent background" in response.data


def test_about_page_loads_with_contact_details(client):
    response = client.get("/about")

    assert response.status_code == 200
    assert b"About us" in response.data
    assert b"248-880-7630" in response.data
    assert b"tel:+12488807630" in response.data
    assert b"stay@moffatbaylodge.example" in response.data
    assert b"Joviedsa Island, Washington" in response.data


def test_attractions_page_loads_with_required_activities(client):
    response = client.get("/attractions")

    assert response.status_code == 200
    assert b"Attractions" in response.data
    assert b"Hiking" in response.data
    assert b"Kayaking" in response.data
    assert b"Whale watching" in response.data
    assert b"Scuba diving" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"service": "moffat-bay", "status": "ok"}
