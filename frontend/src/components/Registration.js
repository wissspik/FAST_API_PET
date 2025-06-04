import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { register } from '../services/api';
import { validateLogin, validatePassword } from '../utils/validation';
import './Registration.css';

const Registration = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    login: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const loginError = validateLogin(formData.login);
    const passwordError = validatePassword(formData.password);

    if (loginError) {
      setError(loginError);
      return;
    }

    if (passwordError) {
      setError(passwordError);
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      await register(formData.login, formData.password, formData.confirmPassword);
      navigate('/login');
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="registration-container">
      <form onSubmit={handleSubmit} className="registration-form">
        <h2>Registration</h2>
        {error && <div className="error-message">{error}</div>}
        <div className="form-group">
          <label>Login:</label>
          <input
            type="text"
            name="login"
            value={formData.login}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label>Confirm Password:</label>
          <input
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Register</button>
        <p>
          Already have an account?{' '}
          <span className="link" onClick={() => navigate('/login')}>
            Login here
          </span>
        </p>
      </form>
    </div>
  );
};

export default Registration; 