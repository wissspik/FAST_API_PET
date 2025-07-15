import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

function Registration() {
  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)
  const navigate = useNavigate()

  const togglePassword = (field) => {
    if (field === 'password') {
      setShowPassword(!showPassword)
    } else {
      setShowConfirm(!showConfirm)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (password !== confirmPassword) {
      alert('Пароли не совпадают!')
      return
    }
    const response = await fetch('http://localhost:8001/registration', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        login: username,
        password,
        confir_password: confirmPassword,
      }),
    })
    if (response.ok) {
      await fetch('http://localhost:8002/visit_time', {
        method: 'POST',
        credentials: 'include',
      })
      navigate('/feed')
    } else {
      const data = await response.json().catch(() => ({}))
      alert(data.detail || 'Registration failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-gray-800 rounded-xl shadow-xl overflow-hidden">
          <div className="bg-gray-900 px-6 py-8 text-center">
            <span className="material-icons text-purple-400 text-5xl">lock</span>
            <h1 className="text-2xl font-bold text-white mt-4">Регистрация</h1>
            <p className="text-gray-400 mt-2">Создайте новый аккаунт</p>
          </div>
          <div className="px-6 py-6">
            <form onSubmit={handleSubmit} id="authForm">
              <div className="mb-4">
                <div className="input-field flex items-center bg-gray-700 rounded-lg px-4 py-3 border border-gray-600">
                  <span className="material-icons text-gray-400 mr-3">email</span>
                  <input
                    type="email"
                    id="email"
                    className="w-full bg-transparent text-white placeholder-gray-500 outline-none"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
              </div>
              <div className="mb-4">
                <div className="input-field flex items-center bg-gray-700 rounded-lg px-4 py-3 border border-gray-600">
                  <span className="material-icons text-gray-400 mr-3">person</span>
                  <input
                    type="text"
                    id="username"
                    className="w-full bg-transparent text-white placeholder-gray-500 outline-none"
                    placeholder="Логин"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
              </div>
              <div className="mb-4">
                <div className="input-field flex items-center bg-gray-700 rounded-lg px-4 py-3 border border-gray-600">
                  <span className="material-icons text-gray-400 mr-3">lock</span>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    id="password"
                    className="w-full bg-transparent text-white placeholder-gray-500 outline-none"
                    placeholder="Пароль"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                  <button
                    type="button"
                    className="text-gray-400 hover:text-white"
                    onClick={() => togglePassword('password')}
                  >
                    <span className="material-icons" id="toggleIcon">
                      {showPassword ? 'visibility' : 'visibility_off'}
                    </span>
                  </button>
                </div>
              </div>
              <div className="mb-6">
                <div className="input-field flex items-center bg-gray-700 rounded-lg px-4 py-3 border border-gray-600">
                  <span className="material-icons text-gray-400 mr-3">lock</span>
                  <input
                    type={showConfirm ? 'text' : 'password'}
                    id="confirmPassword"
                    className="w-full bg-transparent text-white placeholder-gray-500 outline-none"
                    placeholder="Подтвердите пароль"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                  />
                  <button
                    type="button"
                    className="text-gray-400 hover:text-white"
                    onClick={() => togglePassword('confirm')}
                  >
                    <span className="material-icons" id="toggleConfirmIcon">
                      {showConfirm ? 'visibility' : 'visibility_off'}
                    </span>
                  </button>
                </div>
              </div>
              <button
                type="submit"
                className="btn-primary w-full bg-purple-600 text-white py-3 px-4 rounded-lg font-medium"
              >
                Зарегистрироваться
              </button>
              <div className="flex items-center my-6">
                <div className="flex-grow border-t border-gray-600" />
                <span className="mx-4 text-gray-400 text-sm">ИЛИ</span>
                <div className="flex-grow border-t border-gray-600" />
              </div>
              <Link
                to="/login"
                className="block text-center link-secondary text-purple-400 font-medium py-2 px-4 rounded-lg border border-gray-600 hover:border-purple-400 transition"
              >
                Уже есть аккаунт? Войти
              </Link>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Registration
