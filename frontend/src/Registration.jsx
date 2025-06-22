import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './AuthForm.css'

function Registration() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (password !== confirm) {
      alert('Passwords do not match')
      return
    }
    const response = await fetch('http://localhost:8000/registration', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ login: username, password, confir_password: confirm }),
    })
    if (response.ok) {
      navigate('/dashboard')
    } else {
      const data = await response.json().catch(() => ({}))
      alert(data.detail || 'Registration failed')
    }
  }

  return (
    <div className="page">
      <form className="form-container" onSubmit={handleSubmit}>
        <h2>Registration</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
          required
        />
        <button type="submit">Register</button>
        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  )
}

export default Registration
