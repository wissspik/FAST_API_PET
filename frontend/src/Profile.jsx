import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import avatar from './assets/react.svg'
import './Profile.css'
import {
  ProfileIcon,
  FeedIcon,
  MessageIcon,
  PhoneIcon,
  FriendsIcon,
  CommunitiesIcon,
  PhotoIcon,
  MusicIcon,
  VideoIcon,
  GameIcon,
  MarketIcon,
  FilesIcon,
  HelpIcon,
} from './icons.jsx'

function Profile() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    nickname: '',
    name: '',
    login: '',
    age: '',
    city: '',
    gender: '',
  })

  const menuItems = [
    { label: 'Профиль', Icon: ProfileIcon, onClick: () => navigate('/profile') },
    { label: 'Лента', Icon: FeedIcon, onClick: () => navigate('/feed') },
    { label: 'Мессенджер', Icon: MessageIcon },
    { label: 'Звонки', Icon: PhoneIcon },
    { label: 'Друзья', Icon: FriendsIcon },
    { label: 'Сообщества', Icon: CommunitiesIcon },
    { label: 'Фото', Icon: PhotoIcon },
    { label: 'Музыка', Icon: MusicIcon },
    { label: 'Видео', Icon: VideoIcon },
    { label: 'Игры', Icon: GameIcon },
    { label: 'Маркет', Icon: MarketIcon },
    { label: 'Файлы', Icon: FilesIcon },
    { label: 'Помощь', Icon: HelpIcon },
  ]

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!formData.age || isNaN(Number(formData.age))) {
      alert('Возраст должен быть числом')
      return
    }
    await fetch('http://localhost:8000/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    })
  }

  return (
    <div className="profile-page">
      <aside className="sidebar">
        <nav>
          <ul className="menu">
            {menuItems.map((item) => (
              <li
                key={item.label}
                className="menu-item"
                onClick={item.onClick}
              >
                <item.Icon className="icon-svg" />
                <span className="label">{item.label}</span>
              </li>
            ))}
          </ul>
        </nav>
      </aside>
      <main className="main-area">
        <div className="photo-question">
          <img src={avatar} alt="avatar" className="profile-photo" />
          <div className="question">?</div>
        </div>
        <form className="profile-form" onSubmit={handleSubmit}>
          <input
            type="text"
            name="nickname"
            placeholder="Ник"
            value={formData.nickname}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="name"
            placeholder="Имя"
            value={formData.name}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="login"
            placeholder="Логин"
            value={formData.login}
            onChange={handleChange}
            required
          />
          <input
            type="number"
            name="age"
            placeholder="Возраст"
            value={formData.age}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="city"
            placeholder="Город"
            value={formData.city}
            onChange={handleChange}
            required
          />
          <select
            name="gender"
            value={formData.gender}
            onChange={handleChange}
            required
          >
            <option value="">Пол</option>
            <option value="male">Мужской</option>
            <option value="female">Женский</option>
            <option value="other">Другое</option>
          </select>
          <button type="submit">Заполнить профиль</button>
        </form>
      </main>
    </div>
  )
}

export default Profile
