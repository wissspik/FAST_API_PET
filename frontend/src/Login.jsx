import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './Login.css'

function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    const checkAuth = async () => {
      const res = await fetch('http://localhost:8000/protected', {
        credentials: 'include',
      })

      if (res.ok) {
        navigate('/feed')
        return
      }

      const refreshRes = await fetch('http://localhost:8000/refresh', {
        credentials: 'include',
      })

      if (!refreshRes.ok) return

      const verify = await fetch('http://localhost:8000/protected', {
        credentials: 'include',
      })

      if (verify.ok) {
        navigate('/feed')
      }
    }
    checkAuth()
  }, [navigate])

  const handleSubmit = async (e) => {
    e.preventDefault()
    const response = await fetch('http://localhost:8000/entrance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ login: username, password }),
    })
    if (response.ok) {
      navigate('/feed')
    } else {
      const data = await response.json().catch(() => ({}))
      alert(data.detail || 'Login failed')
    }
  }

  const togglePassword = () => setShowPassword((prev) => !prev)

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-[#1E1E1E] login-container">
      <div className="w-full max-w-md">
        <div className="bg-gray-800 rounded-xl shadow-xl overflow-hidden">
          <div className="bg-gray-900 px-6 py-8 text-center">
            <span className="material-icons text-purple-400 text-5xl">lock</span>
            <h1 className="text-2xl font-bold text-white mt-4">Вход в систему</h1>
            <p className="text-gray-400 mt-2">Введите свои учетные данные</p>
          </div>
          <div className="px-6 py-6">
            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <div className="input-field flex items-center bg-gray-700 rounded-lg px-4 py-3 border border-gray-600">
                  <span className="material-icons text-gray-400 mr-3">person</span>
                  <input
                    type="text"
                    className="w-full bg-transparent text-white placeholder-gray-500 outline-none"
                    placeholder="Логин или Email"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
              </div>
              <div className="mb-6">
                <div className="input-field flex items-center bg-gray-700 rounded-lg px-4 py-3 border border-gray-600">
                  <span className="material-icons text-gray-400 mr-3">lock</span>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    className="w-full bg-transparent text-white placeholder-gray-500 outline-none"
                    placeholder="Пароль"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                  <button type="button" className="text-gray-400 hover:text-white" onClick={togglePassword}>
                    <span className="material-icons">
                      {showPassword ? 'visibility' : 'visibility_off'}
                    </span>
                  </button>
                </div>
              </div>
              <div className="flex justify-end mb-6">
                <a href="#" className="text-sm link-secondary text-purple-400">
                  Забыли пароль?
                </a>
              </div>
              <button type="submit" className="btn-primary w-full bg-purple-600 text-white py-3 px-4 rounded-lg font-medium">
                Войти
              </button>
              <div className="flex items-center my-6">
                <div className="flex-grow border-t border-gray-600"></div>
                <span className="mx-4 text-gray-400 text-sm">ИЛИ</span>
                <div className="flex-grow border-t border-gray-600"></div>
              </div>
              <Link
                to="/registration"
                className="block text-center link-secondary text-purple-400 font-medium py-2 px-4 rounded-lg border border-gray-600 hover:border-purple-400 transition"
              >
                Создать новый аккаунт
              </Link>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
