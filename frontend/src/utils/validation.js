export function checkPassword(password) {
  const len = password.length;
  if (!(len >= 8 && len <= 36)) return false;
  if (!/[A-Z]/.test(password)) return false;
  if (!/[a-z]/.test(password)) return false;
  if (!/\d/.test(password)) return false;
  if (!/[^A-Za-z0-9\s]/.test(password)) return false;
  if (/\s/.test(password)) return false;
  return true;
}

export function checkLogin(login) {
  const len = login.length;
  if (!(len >= 8 && len <= 36)) return false;
  if (!/[a-z]/.test(login)) return false;
  return true;
}