import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
});

// Добавляем перехватчик запросов для установки токена
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Добавляем перехватчик ответов для обработки ошибок авторизации
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Если получаем 401 ошибку (Unauthorized), пробуем обновить токен
    if (error.response?.status === 401) {
      try {
        // Пытаемся обновить токен
        const refreshResponse = await axios.get('/refresh', { withCredentials: true });
        
        // Если успешно обновили токен
        if (refreshResponse.status === 200) {
          // Если оригинальный запрос был на /protected, делаем новый запрос
          if (error.config.url === '/protected') {
            return api.get('/protected');
          }
          
          // Для других запросов повторяем оригинальный запрос
          return api(error.config);
        }
      } catch (refreshError) {
        // Если не удалось обновить токен, перенаправляем на страницу входа
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login';
        }
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;