const API_URL = 'http://localhost:8000';

export const register = async (login, password, confirmPassword) => {
  try {
    const response = await fetch(`${API_URL}/registration`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        login,
        password,
        confir_password: confirmPassword,
      }),
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.detail || 'Registration failed');
    }

    return data;
  } catch (error) {
    throw error;
  }
};

export const login = async (login, password) => {
  try {
    const response = await fetch(`${API_URL}/entrance`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        login,
        password,
      }),
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.detail || 'Login failed');
    }

    return data;
  } catch (error) {
    throw error;
  }
}; 