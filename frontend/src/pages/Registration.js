import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import { checkLogin, checkPassword } from '../utils/validation';

export default function Registration() {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    if (!checkLogin(login)) return setError('Login must be 8–36 chars with lowercase');
    if (!checkPassword(password)) return setError('Password complexity requirements not met');
    if (password !== confirm) return setError('Passwords do not match');

    try {
      await axios.post('/registration', { login, password }, { withCredentials: true });
      navigate('/dashboard');
    } catch {
      setError('Registration failed');
    }
  };

  return (
    <div className="w-full max-w-md bg-white p-8 rounded shadow">
      <h2 className="text-2xl mb-6 text-center">Registration</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input value={login} onChange={e => setLogin(e.target.value)} type="text" placeholder="Login" className="w-full p-2 border rounded" required />
        <input value={password} onChange={e => setPassword(e.target.value)} type="password" placeholder="Password" className="w-full p-2 border rounded" required />
        <input value={confirm} onChange={e => setConfirm(e.target.value)} type="password" placeholder="Confirm Password" className="w-full p-2 border rounded" required />
        <button type="submit" className="w-full py-2 bg-green-600 text-white rounded">Register</button>
      </form>
      <div className="mt-4 text-center">
        <Link to="/login" className="text-blue-600">Back to Login</Link>
      </div>
    </div>
  );
}