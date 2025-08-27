import pytest
from starlette.testclient import TestClient

from auth_service.tests.conftest import client

@pytest.mark.asyncio
async def test_index(client):
    response = client.post("/Test")
    assert response.status_code == 200
