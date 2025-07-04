import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import './Profile.css'
import {
  ProfileIcon,
  FeedIcon,
  MessageIcon,
  HelpIcon,
  SettingsIcon,
  LogoutIcon,
  StatsIcon,
} from './icons.jsx'

function Profile() {
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [name, setName] = useState('')
  const [surname, setSurname] = useState('')
  const [patronymic, setPatronymic] = useState('')
  const [age, setAge] = useState('')
  const [city, setCity] = useState('')
  const [gender, setGender] = useState('Мужской')
  const fileInputRef = useRef(null)

  const menuItems = [
    { label: 'Профиль', Icon: ProfileIcon, onClick: () => navigate('/profile') },
    { label: 'Лента', Icon: FeedIcon, onClick: () => navigate('/feed') },
    { label: 'Мессенджер', Icon: MessageIcon },
    { label: 'Помощь', Icon: HelpIcon },
  ]

  const handleUploadClick = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    formData.append('data', JSON.stringify({ user_id: 1 }))
    try {
      await fetch('http://localhost:8001/profile/data', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      })
    } catch (err) {
      console.error(err)
    }
  }

  const handleLogout = async () => {
    await fetch('http://localhost:8000/logout', {
      method: 'POST',
      credentials: 'include',
    })
    navigate('/login')
  }

  const handleProfileSubmit = async (e) => {
    e.preventDefault()
    try {
      await fetch('http://localhost:8001/profile/put_data_profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          name,
          surname,
          patronymic,
          gender,
          city,
          age: Number(age),
        }),
      })
      setShowForm(false)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="bg-dark-900 text-gray-200 min-h-screen flex">
      <div className="left-column w-64 bg-dark-800 flex-shrink-0 h-screen sticky top-0 overflow-y-auto">
        <div className="p-4 border-b border-dark-700">
          <h1 className="text-xl font-bold text-center">Graut :)</h1>
        </div>
        <nav className="mt-6 space-y-1">
          {/* eslint-disable-next-line no-unused-vars */}
          {menuItems.map(({ label, Icon: ItemIcon, onClick }) => (
            <div
              key={label}
              className="flex items-center px-6 py-3 cursor-pointer hover:bg-white/5 transition"
              onClick={onClick}
            >
              <ItemIcon className="w-6 mr-3" />
              <span className="menu-text">{label}</span>
            </div>
          ))}
        </nav>
      </div>

      <div className="divider w-px bg-white/10" />

      <main className="flex-1 bg-dark-900 p-6 overflow-y-auto">
        <div className="profile-container mx-auto">
          <div className="profile-card">
            <div className="profile-photo">
              <div className="photo-placeholder">
                <i className="fas fa-user-circle" />
              </div>
              <input
                type="file"
                accept="image/*"
                ref={fileInputRef}
                className="hidden"
                onChange={handleFileChange}
              />
              <button className="upload-btn" onClick={handleUploadClick}>
                <i className="fas fa-camera" /> Загрузить фото
              </button>
            </div>
            <div className="profile-info">
              <h2>Профиль пользователя</h2>
              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">Никнейм:</span>
                  <span className="info-value">user123</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Имя:</span>
                  <span className="info-value">Иван</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Фамилия:</span>
                  <span className="info-value">Иванов</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Отчество:</span>
                  <span className="info-value">Иванович</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Возраст:</span>
                  <span className="info-value">25</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Город:</span>
                  <span className="info-value">Москва</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Пол:</span>
                  <span className="info-value">Мужской</span>
                </div>
              </div>
              <button
                className="edit-profile-btn"
                onClick={() => setShowForm(true)}
              >
                <i className="fas fa-edit" /> Заполнить профиль
              </button>
            </div>
          </div>
          <button className="create-post-btn">
            <i className="fas fa-plus-circle" /> Создать пост
          </button>
        </div>
      </main>

      <div className="divider w-px bg-white/10" />

      <div className="right-column w-80 bg-dark-800 flex-shrink-0 h-screen sticky top-0 overflow-y-auto p-4">
        <div className="flex justify-end relative">
          <div
            className="profile-icon w-10 h-10 rounded-full bg-dark-700 flex items-center justify-center cursor-pointer"
            onClick={() => setMenuOpen((v) => !v)}
          >
            <i className="fas fa-user text-lg" />
          </div>
          {menuOpen && (
            <div className="absolute top-12 right-0 bg-dark-700 rounded-md shadow-lg py-2 w-48 z-10">
              <div className="px-4 py-2 hover:bg-dark-600 cursor-pointer flex items-center">
                <StatsIcon className="w-4 mr-3" />
                <span>Статистика</span>
              </div>
              <div className="px-4 py-2 hover:bg-dark-600 cursor-pointer flex items-center">
                <SettingsIcon className="w-4 mr-3" />
                <span>Настройки</span>
              </div>
              <div className="border-t border-dark-600 mt-1" />
              <div
                className="px-4 py-2 hover:bg-dark-600 cursor-pointer text-red-400 flex items-center"
                onClick={handleLogout}
              >
                <LogoutIcon className="w-4 mr-3" />
                <span>Выход</span>
              </div>
            </div>
          )}
        </div>

        <div className="mt-8 p-4 bg-dark-700 rounded-lg hidden md:block">
          <h3 className="font-medium mb-3">Рекомендации</h3>
          <p className="text-sm text-gray-400">Включите уведомления, чтобы не пропустить новые события</p>
          <button className="mt-3 bg-blue-500 hover:bg-blue-600 text-white text-sm px-3 py-1 rounded-md transition">
            Включить
          </button>
        </div>
      </div>
      {showForm && (
        <div className="modal-overlay">
          <div className="modal">
            <button className="close-btn" onClick={() => setShowForm(false)}>
              &times;
            </button>
            <form id="profileForm" onSubmit={handleProfileSubmit}>
              <div className="form-group">
                <label htmlFor="firstName">Имя:</label>
                <input
                  type="text"
                  id="firstName"
                  name="firstName"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor="lastName">Фамилия:</label>
                <input
                  type="text"
                  id="lastName"
                  name="lastName"
                  value={surname}
                  onChange={(e) => setSurname(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor="middleName">Отчество:</label>
                <input
                  type="text"
                  id="middleName"
                  name="middleName"
                  value={patronymic}
                  onChange={(e) => setPatronymic(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor="age">Возраст:</label>
                <input
                  type="number"
                  id="age"
                  name="age"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor="city">Город:</label>
                <input
                  type="text"
                  id="city"
                  name="city"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label>Пол:</label>
                <div>
                  <input
                    type="radio"
                    id="male"
                    name="gender"
                    value="Мужской"
                    checked={gender === 'Мужской'}
                    onChange={(e) => setGender(e.target.value)}
                  />
                  <label htmlFor="male">Мужской</label>
                  <input
                    type="radio"
                    id="female"
                    name="gender"
                    value="Женский"
                    checked={gender === 'Женский'}
                    onChange={(e) => setGender(e.target.value)}
                  />
                  <label htmlFor="female">Женский</label>
                  <input
                    type="radio"
                    id="other"
                    name="gender"
                    value="Другой"
                    checked={gender === 'Другой'}
                    onChange={(e) => setGender(e.target.value)}
                  />
                  <label htmlFor="other">Другой</label>
                </div>
              </div>
              <button type="submit" className="save-btn">Сохранить</button>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Profile
