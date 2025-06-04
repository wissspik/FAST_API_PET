import React, { useEffect, useState } from 'react';
import { authService } from '../services/authService';

const ProtectedRoute = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const isAuth = await authService.checkAuth();
        setIsAuthenticated(isAuth);
      } catch (error) {
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    window.location.href = '/login.html';
    return null;
  }

  return children;
};

export default ProtectedRoute; 