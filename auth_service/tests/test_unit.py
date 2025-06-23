import pytest
from httpx import ASGITransport,AsyncClient
from auth_service.database.models import User
from sqlalchemy import select,func
from auth_service.main import app
from auth_service.database.base import SessionDep
from auth_service.utils.password_val_hash import check_login,check_password
from auth_service.utils.sql_request import get_user_login


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload,expected_status",[
        ({'login':'TestUsers','password':'QWER!10ww','confir_password':'QWER!10ww'},200),
        ({'login':'TestUsers','password':'QWER!10ww','confir_password':'error'},409),
        ({'login':'TestUsers','password':'error','confir_password':'QWER!10ww'},409),
        ({'login':'ooo','password':'QWER!10ww','confir_password':'QWER!10ww'},409),
        ({'login': 'TestUsers', 'password': 'Sugar2220', 'confir_password': 'Sugar2220'}, 409),
        {'login': 'TestUsers', 'password': 'Sugar2220', 'confir_password': 'Sugar2220'}, 409]
)
async def test_registration(session:SessionDep,payload,expected_status):
    async with AsyncClient(transport=ASGITransport(app = app)) as ac:
        response = await ac.post("http://localhost:8000/registration", json=payload)
        if payload['password'] != payload['confir_password']:
            assert response['detail'] == 'Пароли не совпадают'
        elif not check_login(len(payload['login'])):
            assert response['detail'] == 'Введите логин по правилам сайта'
        elif not check_password(payload['password']):
            assert response['detail'] == 'Введите пароль по правилам сайта'
        elif get_user_login(payload['login']) and expected_status != 200:
            assert response['detail'] == 'Пользователь с таким логином уже существует, придумайте другой'
        elif expected_status == 200:
            stmt = select(func.count()).select_from(User)
            result = await session.execute(stmt)
            total_users = result.scalar_one()  # возвращает целое число
            assert response['message'] == 'Успешный логин'
            assert total_users == 1
        assert response.status_code == expected_status
