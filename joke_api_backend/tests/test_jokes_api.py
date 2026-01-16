import pytest


def _assert_error_response(payload: dict) -> None:
    """
    Validate the API's ErrorResponse shape without being too strict about values.
    Expected: {"code": <str>, "message": <str>}
    """
    assert isinstance(payload, dict)
    assert "code" in payload
    assert "message" in payload
    assert isinstance(payload["code"], str)
    assert isinstance(payload["message"], str)
    assert payload["code"].strip() != ""
    assert payload["message"].strip() != ""


def _assert_joke_schema(payload: dict) -> None:
    """
    Validate the API's Joke schema shape.
    Expected: {"id": <int>, "subject": <str>, "setup": <str>, "punchline": <str>}
    """
    assert isinstance(payload, dict)
    for key in ("id", "subject", "setup", "punchline"):
        assert key in payload

    assert isinstance(payload["id"], int)
    assert isinstance(payload["subject"], str)
    assert isinstance(payload["setup"], str)
    assert isinstance(payload["punchline"], str)

    # Ensure non-empty content
    assert payload["subject"].strip() != ""
    assert payload["setup"].strip() != ""
    assert payload["punchline"].strip() != ""


def test_health_check_returns_200_and_expected_payload(client):
    resp = client.get("/")
    assert resp.status_code == 200

    data = resp.json()
    assert isinstance(data, dict)
    # Health check contract from implementation: {"message": "Healthy"}
    assert data.get("message") == "Healthy"


@pytest.mark.asyncio
async def test_get_random_joke_valid_subject_returns_200_and_joke_schema(async_client):
    # Use mixed-case to verify case-insensitive subject handling.
    resp = await async_client.get("/jokes/random", params={"subject": "ProGrAmMiNg"})
    assert resp.status_code == 200

    data = resp.json()
    _assert_joke_schema(data)

    # Subject should match requested subject in a case-insensitive way.
    assert data["subject"].strip().lower() == "programming"


def test_get_random_joke_without_subject_returns_400_error_response(client):
    # The API's OpenAPI indicates 400 for missing subject.
    # FastAPI/Pydantic may return 422 for missing required query params in some setups,
    # but this service is designed/spec'd to return 400, so we assert that contract.
    resp = client.get("/jokes/random")
    assert resp.status_code == 400

    data = resp.json()
    _assert_error_response(data)


def test_get_random_joke_empty_subject_returns_400_error_response(client):
    # Empty string subject should be rejected.
    resp = client.get("/jokes/random?subject=")
    assert resp.status_code == 400

    data = resp.json()
    _assert_error_response(data)


def test_get_random_joke_subject_with_no_jokes_returns_404_error_response(client):
    resp = client.get("/jokes/random", params={"subject": "definitely-not-a-real-subject"})
    assert resp.status_code == 404

    data = resp.json()
    _assert_error_response(data)
