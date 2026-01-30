from backend.entrance.tests.conftest import async_client,db_session
import pytest
from backend.entrance.database.models import User
from sqlalchemy import select
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_payload",
    [
        {
            "login" : "IvanCool321",
            "first_password" : "Abcdefg@",
            "second_password" : "Abcdefg@",
        }
    ]
)
class TestLoginCorrectForm:
        async def test_login(self,async_client,user_payload):
            response = await async_client.post('/registration',json = user_payload)
            print(response.json())
            assert response.status_code  == 200

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_payload",
    [
        { # 1. Не одинаковые пароли
            "login" : "IvanCool321",
            "first_password" : "Abcdefg@",
            "second_password" : "Abcdefg",
        },
        { # 2. Неверный логин
            "login" : "123",
            "first_password" : "IvanCool321",
            "second_password" : "IvanCool321",
        },
        { # 3. 1 пароль некорректный
            "login" : "IvanCool321",
            "first_password" : "123",
            "second_password" : "Ivan123io",
        },
        { # 4. 2 пароль некорректный
            "login" : "IvanCool321",
            "first_password" : "IvanCool321",
            "second_password" : "123",
        },
        { # 5. 1 и 2 пароль некорректные
            "login" : "IvanCool321",
            "first_password" : "123",
            "second_password" : "123",
        },
        { # 6. не корректны все поля
            "login" : 123,
            "first_password" : 123,
            "second_password" : 123,
        },

    ]
)
class TestLoginUncorrectForm:
    async def test_login(self, async_client, user_payload):
        response = await async_client.post('/registration', json=user_payload)
        print(response.json())
        assert response.status_code == 422



@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_payload",
    [
        {
            "login" : "IvanCool321",
            "first_password" : "Abcdefg@",
            "second_password" : "Abcdefg@"
        }
    ]
)
class TestLoginCorrectDb:
    async def test_login(self, db_session, async_client,user_payload):
        response = await async_client.post('/registration', json=user_payload)
        result = await db_session.scalars(select(User))
        count = result.all()
        print(len(count))
        assert len(count) == 1
        assert response.status_code == 200
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_payload",
    [
        { # 1. Не одинаковые пароли
            "login" : "IvanCool321",
            "first_password" : "Abcdefg@",
            "second_password" : "Abcdefg",
        },
        { # 2. Неверный логин
            "login" : "123",
            "first_password" : "IvanCool321",
            "second_password" : "IvanCool321",
        },
        { # 3. 1 пароль некорректный
            "login" : "IvanCool321",
            "first_password" : "123",
            "second_password" : "Ivan123io",
        },
        { # 4. 2 пароль некорректный
            "login" : "IvanCool321",
            "first_password" : "IvanCool321",
            "second_password" : "123",
        },
        { # 5. 1 и 2 пароль некорректные
            "login" : "IvanCool321",
            "first_password" : "123",
            "second_password" : "123",
        },
        { # 6. не корректны все поля
            "login" : 123,
            "first_password" : 123,
            "second_password" : 123,
        },

    ]
)
class TestLoginUncorrectDb:
    async def test_login(self, db_session, async_client,user_payload):
        response = await async_client.post('/registration', json=user_payload)
        result = await db_session.scalars(select(User))
        count = result.all()
        print(len(count))
        assert len(count) == 0