import pytest
from httpx import ASGITransport,AsyncClient
from auth_service.database.models import User
from sqlalchemy import select
from auth_service.main import app
from auth_service.utils.password_val_hash import hash_password
from auth_service.tests.conftest import SessionDep
from auth_service.utils.password_val_hash import check_login,check_password
from auth_service.utils.sql_request import get_user_login
import re

@pytest.fixture
async def existing_user(session: SessionDep):
    # создаём пользователя «TestUser» в БД
    user = User(
        login="TestUsers",
        password_hash=hash_password("QWER!10ww")
    )

    session.add(user)
    await session.commit()
    return user


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload,expected_status",[
        ({'login':'SuccsesUser','password':'QWER!10ww','confir_password':'QWER!10ww'},200),
        ({'login':'TestUsers','password':'QWER!10ww','confir_password':'error'},409),
        ({'login':'TestUsers','password':'error','confir_password':'QWER!10ww'},409),
        ({'login':'ooo','password':'QWER!10ww','confir_password':'QWER!10ww'},409),
        ({'login': 'TestUsers', 'password': 'Sugar2220', 'confir_password': 'Sugar2220'}, 409),
        ({'login': 123, 'password': 'Sugar2220', 'confir_password': 'Sugar2220'}, 409),
        ({'login': 'TestUsers', 'password': 123, 'confir_password': 'Sugar2220'}, 409),
        ({'login': 'TestUsers', 'password': 'Sugar2220', 'confir_password': 123}, 409),
        ({'login': None, 'password': None, 'confir_password': 'Sugar2220'}, 409),
        ({'login': None, 'password': None, 'confir_password': 'Sugar2220'}, 409),
        ({'login':'TestUsers','password':'QWER!10ww','confir_password':'QWER!10ww'},409),
    ]
)
async def test_registration(get_session:SessionDep,payload,expected_status):
    async with AsyncClient(transport=ASGITransport(app = app)) as ac:
        response = await ac.post("http://localhost:8000/registration",json=payload)
    if payload['password'] != payload['confir_password']:
        assert response['detail'] == 'Пароли не совпадают'
        assert response.status_code == expected_status


    elif not check_login(payload['login']) :
        assert response['detail'] == 'Введите логин по правилам сайта'
        assert response.status_code == expected_status

    elif not check_password(payload['password']):
        assert response['detail'] == 'Введите пароль по правилам сайта'
        assert response.status_code == expected_status

    elif  payload['login'] is None or  payload['password'] is None or  payload['confir_password'] is None:
        assert response['detail'] == 'Введите пароль по правилам сайта'
        assert response.status_code == expected_status

    elif response['detail'] == 'Пользователь с таким логином уже существует, придумайте другой':
        assert response.status_code == expected_status
        stml = select(User).filteb_by(login=payload['login'])
        result = await get_session.execute(stml)
        count = result.scalar()
        assert count == 1

