import React, { useState, useEffect } from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import api from '../services/api';

export default function PrivateRoute() {
  const [auth, setAuth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Проверяем аутентификацию через GET /protected
        // Если access_token отсутствует или недействителен, 
        // интерцептор автоматически попытается обновить токен через /refresh
        // и при успехе сделает повторный запрос на /protected
        await api.get('/protected');
        setAuth(true);
      } catch (error) {
        // Если все попытки не удались, считаем пользователя неавторизованным
        setAuth(false);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (loading) {
    return <div className="text-center">Проверка аутентификации...</div>;
  }

  return auth ? <Outlet /> : <Navigate to="/login" replace />;
} 