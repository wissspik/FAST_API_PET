import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

export default function PrivateRoute() {
  // Проверяем наличие cookie с access_token
  const isAuthenticated = document.cookie.includes('access_token');
  
  // Если пользователь не аутентифицирован, перенаправляем на страницу входа
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Если пользователь аутентифицирован, отображаем дочерние маршруты
  return <Outlet />;
}