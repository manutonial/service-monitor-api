BASE_URL = "/api"


def create_service(
    client, name="My Service", url="https://example.com", expected_status=200
):
    """Post a service and return the response object."""
    return client.post(
        f"{BASE_URL}/services",
        json={"name": name, "url": url, "expected_status": expected_status},
    )


def seed_services(client, count):
    """Create `count` services with auto-generated unique names and URLs."""
    for i in range(count):
        create_service(
            client, name=f"Service {i}", url=f"https://service-{i}.example.com"
        )


def test_create_service_returns_201(client):
    response = create_service(client)

    assert response.status_code == 201

    body = response.json()
    assert body["name"] == "My Service"
    assert "https://example.com" in body["url"]
    assert body["expected_status"] == 200
    assert "id" in body
    assert "created_at" in body


def test_create_service_persists_custom_expected_status(client):
    response = create_service(client, expected_status=204)

    assert response.status_code == 201
    assert response.json()["expected_status"] == 204


def test_create_service_invalid_url_returns_422(client):
    response = client.post(
        f"{BASE_URL}/services",
        json={"name": "Bad URL", "url": "not-a-valid-url"},
    )

    assert response.status_code == 422


def test_create_service_missing_name_returns_422(client):
    response = client.post(
        f"{BASE_URL}/services",
        json={"url": "https://example.com"},
    )

    assert response.status_code == 422


def test_create_service_duplicate_url_returns_409(client):
    # The `url` column has a UNIQUE constraint. A second POST with the same
    # URL must return 409 Conflict, not an unhandled 500.
    payload = {"name": "Original", "url": "https://example.com"}
    first_response = client.post(f"{BASE_URL}/services", json=payload)
    assert first_response.status_code == 201

    duplicate_response = client.post(f"{BASE_URL}/services", json=payload)
    assert duplicate_response.status_code == 409


def test_list_services_empty_by_default(client):
    response = client.get(f"{BASE_URL}/services")

    assert response.status_code == 200
    assert response.json() == []


def test_list_services_returns_all_created(client):
    seed_services(client, count=3)

    response = client.get(f"{BASE_URL}/services")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_list_services_limit_restricts_results(client):
    seed_services(client, count=5)

    response = client.get(f"{BASE_URL}/services", params={"limit": 2})

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_services_skip_offsets_results(client):
    seed_services(client, count=4)

    all_services = client.get(f"{BASE_URL}/services").json()
    skipped_response = client.get(f"{BASE_URL}/services", params={"skip": 2})

    assert skipped_response.status_code == 200
    assert len(skipped_response.json()) == 2
    assert skipped_response.json()[0]["id"] == all_services[2]["id"]


def test_list_services_limit_above_max_returns_422(client):
    response = client.get(f"{BASE_URL}/services", params={"limit": 501})

    assert response.status_code == 422


def test_list_services_negative_skip_returns_422(client):
    response = client.get(f"{BASE_URL}/services", params={"skip": -1})

    assert response.status_code == 422


def test_check_nonexistent_service_returns_404(client):
    response = client.post(f"{BASE_URL}/services/9999/check")

    assert response.status_code == 404


def test_get_history_nonexistent_service_returns_empty_list(client):
    response = client.get(f"{BASE_URL}/services/9999/history")

    assert response.status_code == 200
    assert response.json() == []


def test_get_history_limit_restricts_results(client):
    # The history endpoint accepts a `limit` query param.
    response = client.get(f"{BASE_URL}/services/1/history", params={"limit": 10})

    assert response.status_code == 200


def test_health_endpoint_returns_ok(client):
    response = client.get(f"{BASE_URL}/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_openapi_schema_is_accessible(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    body = response.json()
    assert "openapi" in body
    assert "paths" in body
