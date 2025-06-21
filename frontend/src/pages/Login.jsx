import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [login, setLogin] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();



  const handleSubmit = async e => {
    e.preventDefault();
    try {
      await axios.post('/entrance', { login, password }, { withCredentials: true });
      navigate('/dashboard');
    } catch {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="w-full max-w-md bg-white p-8 rounded shadow">
      <h2 className="text-2xl mb-6 text-center">Login</h2>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          value={login}
          onChange={e => setLogin(e.target.value)}
          type="text"
          placeholder="Login"
          className="w-full p-2 border rounded"
          required
        />
        <input
          value={password}
          onChange={e => setPassword(e.target.value)}
          type="password"
          placeholder="Password"
          className="w-full p-2 border rounded"
          required
        />
        <button
          type="submit"
          className="w-full py-2 bg-blue-600 text-white rounded"
        >
          Sign In
        </button>
      </form>
      <div className="mt-4 flex justify-between">
        <Link to="/registration" className="text-blue-600">Register</Link>
        <div className="space-x-2">
          <a href="/auth/github" className="px-3 py-1 bg-gray-800 text-white rounded">GitHub</a>
          <a href="/auth/google" className="px-3 py-1 bg-red-500 text-white rounded">Google</a>
        </div>
      </div>
    </div>
  );
}
