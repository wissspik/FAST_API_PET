import React, { useState, useEffect } from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import api from '../services/api';

export default function PrivateRoute() {
  const [auth, setAuth] = useState(null);

  useEffect(() => {
    api.get('/entrance')
      .then(() => setAuth(true))
      .catch(() => setAuth(false));
  }, []);

  if (auth === null) {
    return <div className="text-center">Checking authentication...</div>;
  }

  return auth ? <Outlet /> : <Navigate to="/login" replace />;
} 