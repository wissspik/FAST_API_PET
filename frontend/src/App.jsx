import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login.jsx';
import Registration from './pages/Registration.jsx';
import Dashboard from './components/Dashboard';
import PrivateRoute from './components/PrivateRoute.jsx';
import Tape from './components/Tape.jsx';

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/registration" element={<Registration />} />
        <Route element={<PrivateRoute />}> 
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/tape" element={<Tape />} />
        </Route>
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </div>
  );
} 