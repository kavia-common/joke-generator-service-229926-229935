import os
import sys

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

# Ensure imports like `from src.api.main import app` work when tests are run from repo root.
_CONTAINER_ROOT = os.path.dirname(os.path.dirname(__file__))
if _CONTAINER_ROOT not in sys.path:
    sys.path.insert(0, _CONTAINER_ROOT)


@pytest.fixture(scope="session")
def app():
    """FastAPI app instance for tests."""
    from src.api.main import app as fastapi_app

    return fastapi_app


@pytest.fixture()
def client(app):
    """Synchronous FastAPI TestClient fixture."""
    with TestClient(app) as c:
        yield c


@pytest.fixture()
async def async_client(app):
    """Async HTTPX client fixture for the ASGI app (no real network)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
