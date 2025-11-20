import re

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

def check_login(login: str) -> bool:
    if not (8 <= len(login) <= 36):
        return False
    if re.search(r"[a-z]", login) is None:
        return False
    return True

def check_password(password: str) -> bool:
    patter = r'[A-Za-z@$!%*?&]{8,24}'
    return bool(re.match(patter, password))

ph = PasswordHasher()

# 1. Хэширование
def hash_password(plain_password: str) -> str:
    return ph.hash(plain_password)

# 2. Проверка
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False