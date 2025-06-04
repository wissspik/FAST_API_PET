import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

// Create axios instance with credentials
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});

// Add response interceptor for handling 401 errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If error is 401 and we haven't tried to refresh token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Try to refresh token
        await api.post('/refresh');
        // Retry the original request
        return api(originalRequest);
      } catch (refreshError) {
        // If refresh fails, redirect to login
        window.location.href = '/login.html';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export const authService = {
  // Check if user is authenticated
  async checkAuth() {
    try {
      const response = await api.get('/protected');
      return response.status === 200;
    } catch (error) {
      return false;
    }
  },

  // Login user
  async login(login, password) {
    try {
      const response = await api.post('/entrance', { login, password });
      if (response.status === 200) {
        window.location.href = '/dashboard.html';
      }
      return response;
    } catch (error) {
      if (error.response?.status === 409) {
        throw new Error('Неверный логин или пароль');
      }
      throw error;
    }
  },

  // Refresh token
  async refreshToken() {
    try {
      const response = await api.post('/refresh');
      return response.status === 200;
    } catch (error) {
      window.location.href = '/login.html';
      return false;
    }
  },

  // Logout user
  async logout() {
    try {
      await api.post('/logout');
      window.location.href = '/login.html';
    } catch (error) {
      console.error('Logout error:', error);
    }
  }
}; 