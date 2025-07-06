import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
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

async function getUserId() {
  const auth = await fetch('http://localhost:8001/protected', {
    credentials: 'include',
  })
  if (auth.ok) {
    const { user_id } = await auth.json()
    return user_id
  }

  const refreshRes = await fetch('http://localhost:8001/refresh', {
    credentials: 'include',
  })
  if (!refreshRes.ok) return null

  const verify = await fetch('http://localhost:8001/protected', {
    credentials: 'include',
  })
  if (!verify.ok) return undefined
  const { user_id } = await verify.json()
  return user_id
}

function Feed() {
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)
  const [currentUserId, setCurrentUserId] = useState(null)

  useEffect(() => {
    const checkAuth = async () => {
      const id = await getUserId()
      if (id === null) {
        navigate('/login')
        return
      }
      if (id !== undefined) setCurrentUserId(id)
    }

    checkAuth()
  }, [navigate])

  const handleLogout = async () => {
    await fetch('http://localhost:8001/logout', {
      method: 'POST',
      credentials: 'include',
    })
    navigate('/login')
  }

  const menuItems = [
    {
      label: 'Профиль',
      Icon: ProfileIcon,
      onClick: () => {
        if (currentUserId) navigate(`/profile/${currentUserId}`)
      },
    },
    { label: 'Лента', Icon: FeedIcon },
    { label: 'Мессенджер', Icon: MessageIcon },
    { label: 'Помощь', Icon: HelpIcon },
  ]

  return (
    <div className="bg-dark-900 text-gray-200 min-h-screen flex">
      <div className="left-column w-64 bg-dark-800 flex-shrink-0 h-screen sticky top-0 overflow-y-auto">
        <div className="p-4 border-b border-dark-700">
          <h1 className="text-xl font-bold text-center">Graut :)</h1>
        </div>
        <nav className="mt-6 space-y-1">
          {/* eslint-disable-next-line no-unused-vars */}
          {menuItems.map(({ label, Icon: MenuIcon, onClick }) => (
            <div
              key={label}
              className="menu-item flex items-center px-6 py-3 cursor-pointer hover:bg-white/5 transition"
              onClick={onClick}
            >
              <MenuIcon className="w-6 mr-3" />
              <span className="menu-text">{label}</span>
            </div>
          ))}
        </nav>
      </div>

      <div className="divider w-px bg-white/10" />

      <main className="flex-1 bg-dark-900 p-6 overflow-y-auto">
        <div className="max-w-4xl mx-auto h-full flex flex-col items-center justify-center">
          <div className="text-center">
            <i className="fas fa-compass text-5xl text-gray-600 mb-4" />
            <h2 className="text-2xl font-semibold text-gray-400">Выберите раздел</h2>
            <p className="text-gray-500 mt-2">Начните с выбора раздела в меню слева</p>
          </div>
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
            <div className="dropdown absolute top-12 right-0 bg-dark-700 rounded-md shadow-lg py-2 w-48 z-10">
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
    </div>
  )
}

export default Feed
