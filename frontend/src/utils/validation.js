export const validateLogin = (login) => {
  if (!(8 <= login.length && login.length <= 36)) {
    return 'Login must be between 8 and 36 characters';
  }
  if (!/[a-z]/.test(login)) {
    return 'Login must contain at least one lowercase letter';
  }
  return '';
};

export const validatePassword = (password) => {
  if (!(8 <= password.length && password.length <= 36)) {
    return 'Password must be between 8 and 36 characters';
  }
  if (!/[A-Z]/.test(password)) {
    return 'Password must contain at least one uppercase letter';
  }
  if (!/[a-z]/.test(password)) {
    return 'Password must contain at least one lowercase letter';
  }
  if (!/\d/.test(password)) {
    return 'Password must contain at least one number';
  }
  if (!/[^A-Za-z0-9\s]/.test(password)) {
    return 'Password must contain at least one special character';
  }
  if (/\s/.test(password)) {
    return 'Password cannot contain spaces';
  }
  return '';
}; 