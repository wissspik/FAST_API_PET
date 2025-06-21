import { useState } from 'react'
import { Link } from 'react-router-dom'
import './AuthForm.css'

function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    // TODO: handle login
  }

  return (
    <div className="page">
      <form className="form-container" onSubmit={handleSubmit}>
        <h2>Login</h2>
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
        <button type="submit">Login</button>
        <div className="oauth-buttons">
          <a href="/auth/google" className="oauth-btn google">Google</a>
          <a href="/auth/github" className="oauth-btn github">GitHub</a>
        </div>
        <p>
          Don't have an account?{' '}
          <Link to="/registration">Register</Link>
        </p>
      </form>
    </div>
  )
}

export default Login
