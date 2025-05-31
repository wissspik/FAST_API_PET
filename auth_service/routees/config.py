import re

def check_password(password: str) -> bool:
    if not (8 <= len(password) <= 36):
        return False
    if re.search(r'[A-Z]', password) is None:   return False
    if re.search(r'[a-z]', password) is None:   return False
    if re.search(r'\d', password) is None:    return False
    if re.search(r'[^A-Za-z0-9\s]', password) is None: return False
    if re.search(r'\s', password) is not None: return False
    return True
