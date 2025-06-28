import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import avatar from './assets/react.svg'
import './Feed.css'
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
  SettingsIcon,
  LogoutIcon,
  StatsIcon,
} from './icons.jsx'

function Feed() {
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const checkAuth = async () => {
      const res = await fetch('http://localhost:8000/protected', {
        credentials: 'include',
      })

      if (res.ok) return

      const refreshRes = await fetch('http://localhost:8000/refresh', {
        credentials: 'include',
      })

      if (!refreshRes.ok) {
        navigate('/login')
        return
      }

      const verify = await fetch('http://localhost:8000/protected', {
        credentials: 'include',
      })

      if (!verify.ok) {
        navigate('/login')
      }
    }

    checkAuth()
  }, [navigate])

  const handleLogout = async () => {
    await fetch('http://localhost:8000/logout', {
      method: 'POST',
      credentials: 'include',
    })
    navigate('/login')
  }

  const menuItems = [
    { label: 'Профиль', Icon: ProfileIcon, onClick: () => navigate('/profile') },
    { label: 'Лента', Icon: FeedIcon },
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

  return (
    <div className="feed-page">
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
        <header className="profile-header">
          <div className="profile-block" onClick={() => setMenuOpen((v) => !v)}>
            <img src={avatar} alt="avatar" className="avatar" />
            <span className="name">Имя Пользователя</span>
            <span className="arrow">▼</span>
          </div>
          {menuOpen && (
            <div className="profile-menu">
              <div className="profile-menu-item">
                <SettingsIcon className="icon-svg" />
                <span>Настройки</span>
              </div>
              <div className="profile-menu-item" onClick={handleLogout}>
                <LogoutIcon className="icon-svg" />
                <span>Выход</span>
              </div>
              <div className="profile-menu-item">
                <StatsIcon className="icon-svg" />
                <span>Статистика</span>
              </div>
            </div>
          )}
        </header>
        <section className="stories-placeholder" />
        <section className="feed-placeholder">
          <p>Здесь будет лента</p>
        </section>
        <section className="player-placeholder" />
      </main>
    </div>
  )
}

export default Feed
