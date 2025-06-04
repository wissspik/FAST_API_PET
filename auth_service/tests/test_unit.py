import pytest
from httpx import ASGITransport,AsyncClient

from auth_service.main import app



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload,expected_status",[
        ({'login':'TestUsers','password':'QWER!10ww','confir_password':'QWER!10ww'},200),
        ({'login':'TestUsers','password':'QWER!10ww','confir_password':'error'},409),
        ({'login':'TestUsers','password':'error','confir_password':'QWER!10ww'},409),
        ({'login':'ooo','password':'QWER!10ww','confir_password':'QWER!10ww'},409),
        ({'login': 'TestUsers', 'password': 'Sugar2220', 'confir_password': 'Sugar2220'}, 409),]
)
async def test_registration(payload,expected_status):
    async with AsyncClient(transport=ASGITransport(app = app)) as ac:
        response = await ac.post("/registration")
        assert response.status_code == expected_status
