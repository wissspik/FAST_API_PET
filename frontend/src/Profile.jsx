import { useState, useRef, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
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

const tagOptions = [
  { value: 'Программирование', icon: 'fas fa-code' },
  { value: 'Дизайн', icon: 'fas fa-paint-brush' },
  { value: 'Фотография', icon: 'fas fa-camera' },
  { value: 'Музыка', icon: 'fas fa-music' },
  { value: 'Путешествия', icon: 'fas fa-plane' },
  { value: 'Кулинария', icon: 'fas fa-utensils' },
  { value: 'Спорт', icon: 'fas fa-running' },
  { value: 'Книги', icon: 'fas fa-book' },
  { value: 'Игры', icon: 'fas fa-gamepad' },
  { value: 'Наука', icon: 'fas fa-atom' },
  { value: 'Искусство', icon: 'fas fa-palette' },
  { value: 'Технологии', icon: 'fas fa-microchip' },
]

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

function Profile() {
  const navigate = useNavigate()
  const { userId } = useParams()
  const [currentUserId, setCurrentUserId] = useState(null)
  const isOwnProfile = !userId || Number(userId) === currentUserId
  const [menuOpen, setMenuOpen] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [status, setStatus] = useState('unactivate')

  const sendVisit = async () => {
    await fetch('http://localhost:8002/record_visit_time', {
      method: 'POST',
      credentials: 'include',
    })
  }
  const [notFound, setNotFound] = useState(false)

  const [name, setName] = useState('')
  const [surname, setSurname] = useState('')
  const [patronymic, setPatronymic] = useState('')
  const [age, setAge] = useState('')
  const [city, setCity] = useState('')
  const genderMap = {
    male: 'Мужской',
    female: 'Женский',
    other: 'Другой',
  }

  const [gender, setGender] = useState('male')
  const [login, setLogin] = useState('')

  const [editName, setEditName] = useState('')
  const [editSurname, setEditSurname] = useState('')
  const [editPatronymic, setEditPatronymic] = useState('')
  const [editAge, setEditAge] = useState('')
  const [editCity, setEditCity] = useState('')
  const [editGender, setEditGender] = useState('male')

  const [showArticleForm, setShowArticleForm] = useState(false)
  const [articleTitle, setArticleTitle] = useState('')
  const [articleSubtitle, setArticleSubtitle] = useState('')
  const [articleContent, setArticleContent] = useState('')
  const [articleTags, setArticleTags] = useState([])
  const [articles, setArticles] = useState([])

  const fileInputRef = useRef(null)
  const [photoSrc, setPhotoSrc] = useState(null)

  const fetchArticles = async (id) => {
    try {
      const res = await fetch(
        `http://localhost:8003/profile/take_article?user_id=${id}`,
        {
          method: 'POST',
          credentials: 'include',
        },
      )
      if (res.ok) {
        const data = await res.json()
        setArticles(data)
      } else {
        setArticles([])
      }
    } catch (err) {
      console.error(err)
    }
  }

  useEffect(() => {
    const init = async () => {
      const idFromProtected = await getUserId()
      if (idFromProtected === null) {
        navigate('/login')
        return
      }

      if (idFromProtected !== undefined) setCurrentUserId(idFromProtected)

      await sendVisit()

      const id = userId || idFromProtected

      if (!userId && id) {
        navigate(`/profile/${id}`, { replace: true })
      }
    }

    init()
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!currentUserId) return

    const fetchProfile = async () => {
      const id = userId || currentUserId
      const profileRes = await fetch(`http://localhost:8002/profile/${id}`, {
        credentials: 'include',
      })
      if (profileRes.ok) {
        const user_data = await profileRes.json()
        setLogin(user_data.login || '')
        setName(user_data.name || '')
        setSurname(user_data.surname || '')
        setPatronymic(user_data.patronymic || '')
        setAge(String(user_data.age || ''))
        setCity(user_data.city || '')
        setGender(user_data.gender || 'male')
        if (user_data.file && user_data.mime_type) {
          setPhotoSrc(`data:${user_data.mime_type};base64,${user_data.file}`)
        } else {
          setPhotoSrc(null)
        }

        setEditName(user_data.name || '')
        setEditSurname(user_data.surname || '')
        setEditPatronymic(user_data.patronymic || '')
        setEditAge(String(user_data.age || ''))
        setEditCity(user_data.city || '')
        setEditGender(user_data.gender || 'male')
        setNotFound(false)
        const statusRes = await fetch(
          `http://localhost:8002/check_time?user_id=${id}`,
          { method: 'POST' },
        )
        if (statusRes.ok) {
          const { status } = await statusRes.json()
          setStatus(status)
        }
        await fetchArticles(id)
      } else {
        setNotFound(true)
      }
    }

    fetchProfile()
  }, [currentUserId]) // eslint-disable-line react-hooks/exhaustive-deps

  const menuItems = [
    {
      label: 'Профиль',
      Icon: ProfileIcon,
      onClick: () => {
        sendVisit()
        if (currentUserId) navigate(`/profile/${currentUserId}`)
      },
    },
    { label: 'Лента', Icon: FeedIcon, onClick: () => { sendVisit(); navigate('/feed') } },
    { label: 'Мессенджер', Icon: MessageIcon, onClick: sendVisit },
    { label: 'Помощь', Icon: HelpIcon },
  ]

  const openForm = () => {
    setEditName(name)
    setEditSurname(surname)
    setEditPatronymic(patronymic)
    setEditAge(age)
    setEditCity(city)
    setEditGender(gender)
    setShowForm(true)
  }

  const handleUploadClick = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    try {
      await fetch(`http://localhost:8002/profile/upload_photo?user_id=${currentUserId}`, {
        method: 'POST',
        body: formData,
        credentials: 'include',
      })
      setPhotoSrc(URL.createObjectURL(file))
    } catch (err) {
      console.error(err)
    }
  }

  const handleLogout = async () => {
    await fetch('http://localhost:8001/logout', {
      method: 'POST',
      credentials: 'include',
    })
    navigate('/login')
  }

  const handleProfileSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch('http://localhost:8002/profile/change_profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          user_id: currentUserId,
          name: editName,
          surname: editSurname,
          patronymic: editPatronymic,
          gender: editGender,
          city: editCity,
          age: Number(editAge),
        }),
      })
      if (res.ok) {
        setName(editName)
        setSurname(editSurname)
        setPatronymic(editPatronymic)
        setGender(editGender)
        setCity(editCity)
        setAge(editAge)
        setShowForm(false)
        await sendVisit()
      }
    } catch (err) {
      console.error(err)
    }
  }

  const handleTagChange = (value) => {
    setArticleTags((prev) => {
      if (prev.includes(value)) {
        return prev.filter((t) => t !== value)
      }
      if (prev.length >= 5) {
        alert('Можно выбрать максимум 5 интересов')
        return prev
      }
      return [...prev, value]
    })
  }

  const handleArticleSubmit = async (e) => {
    e.preventDefault()
    if (articleTags.length > 5) {
      alert('Пожалуйста, выберите не более 5 интересов')
      return
    }
    const data = {
      title: articleTitle,
      subtitle: articleSubtitle,
      content: articleContent,
      tags: articleTags,
    }
    try {
      const res = await fetch('http://localhost:8003/profile/create_article', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(data),
      })
      if (res.ok) {
        await fetchArticles(currentUserId)
        alert('Статья успешно создана!')
      }
    } catch (err) {
      console.error(err)
    }
    setShowArticleForm(false)
    setArticleTitle('')
    setArticleSubtitle('')
    setArticleContent('')
    setArticleTags([])
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
        {notFound ? (
          <div className="flex items-center justify-center h-full text-xl">
            Такого пользователя нет
          </div>
        ) : (
        <div className="profile-container mx-auto">
          <div className="profile-card">
            <div className="profile-photo">
              <div className="photo-placeholder">
                {photoSrc ? (
                  <img src={photoSrc} alt="avatar" className="photo-img" />
                ) : (
                  <i className="fas fa-user-circle" />
                )}
                <span
                  className={`status-dot ${status === 'activate' ? 'bg-green-500' : 'bg-gray-500'}`}
                />
              </div>
              {isOwnProfile && (
                <>
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
                </>
              )}
            </div>
            <div className="profile-info">
              <h2>Профиль пользователя</h2>
              <div className="info-grid">
                <div className="info-item">
                  <span className="info-label">Никнейм:</span>
                  <span className="info-value">{login}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Имя:</span>
                  <span className="info-value">{name}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Фамилия:</span>
                  <span className="info-value">{surname}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Отчество:</span>
                  <span className="info-value">{patronymic}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Возраст:</span>
                  <span className="info-value">{age}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Город:</span>
                  <span className="info-value">{city}</span>
                </div>
                <div className="info-item">
                  <span className="info-label">Пол:</span>
                  <span className="info-value">{genderMap[gender] || gender}</span>
                </div>
              </div>
              {isOwnProfile ? (
                <>
                  <button
                    className="edit-profile-btn"
                    onClick={openForm}
                  >
                    <i className="fas fa-edit" /> Заполнить профиль
                  </button>
                  <button
                    className="write-article-btn"
                    onClick={() => setShowArticleForm(true)}
                  >
                    <i className="fas fa-pen" /> Написать статью
                  </button>
                </>
              ) : null}
            </div>
          </div>
          {!isOwnProfile && (
            <div className="friend-actions">
              <button className="add-friend-btn">Добавить в друзья</button>
              <button className="send-message-btn">Написать сообщение</button>
            </div>
          )}
          <div className="articles-container mt-6 space-y-4">
            {articles.map((a, idx) => (
              <div key={idx} className="article-tile p-4 rounded-lg relative">
                <div className="article-options">
                  <i className="fas fa-ellipsis-h" />
                </div>
                <h3 className="text-xl font-bold mb-1">{a.title}</h3>
                <h4 className="text-gray-300 mb-2">{a.subtitle}</h4>
                <p className="text-gray-200 mb-2">{a.content}</p>
                <div className="flex flex-wrap gap-2">
                  {a.tags?.map((t) => (
                    <span key={t} className="tag bg-gray-600 px-2 py-1 rounded text-sm">
                      {t}
                    </span>
                  ))}
                </div>
                <div className="article-actions">
                  <button className="action-btn like-btn">
                    <i className="far fa-heart mr-1" /> Лайк
                  </button>
                  <button className="action-btn comment-btn">
                    <i className="far fa-comment mr-1" /> Комментарий
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
        )}
      </main>

      <div className="divider w-px bg-white/10" />

      <div className="right-column w-80 bg-dark-800 flex-shrink-0 h-screen sticky top-0 overflow-y-auto p-4">
        <div className="flex justify-end relative">
          <div
            className="profile-icon w-10 h-10 rounded-full bg-dark-700 flex items-center justify-center cursor-pointer"
            onClick={() => {
              sendVisit()
              setMenuOpen((v) => !v)
            }}
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
                  value={editName}
                  onChange={(e) => setEditName(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor="lastName">Фамилия:</label>
                <input
                  type="text"
                  id="lastName"
                  name="lastName"
                  value={editSurname}
                  onChange={(e) => setEditSurname(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor="middleName">Отчество:</label>
                <input
                  type="text"
                  id="middleName"
                  name="middleName"
                  value={editPatronymic}
                  onChange={(e) => setEditPatronymic(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor="age">Возраст:</label>
                <input
                  type="number"
                  id="age"
                  name="age"
                  value={editAge}
                  onChange={(e) => setEditAge(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label htmlFor="city">Город:</label>
                <input
                  type="text"
                  id="city"
                  name="city"
                  value={editCity}
                  onChange={(e) => setEditCity(e.target.value)}
                />
              </div>
                <div className="form-group">
                <label>Пол:</label>
                <div>
                  <input
                    type="radio"
                    id="male"
                    name="gender"
                    value="male"
                    checked={editGender === 'male'}
                    onChange={(e) => setEditGender(e.target.value)}
                  />
                  <label htmlFor="male">Мужской</label>
                  <input
                    type="radio"
                    id="female"
                    name="gender"
                    value="female"
                    checked={editGender === 'female'}
                    onChange={(e) => setEditGender(e.target.value)}
                  />
                  <label htmlFor="female">Женский</label>
                  <input
                    type="radio"
                    id="other"
                    name="gender"
                    value="other"
                    checked={editGender === 'other'}
                    onChange={(e) => setEditGender(e.target.value)}
                  />
                  <label htmlFor="other">Другой</label>
                </div>
              </div>
              <button type="submit" className="save-btn">Сохранить</button>
            </form>
          </div>
        </div>
      )}
      {showArticleForm && (
        <div className="modal-overlay">
          <div className="modal article-modal">

            <button className="close-btn" onClick={() => setShowArticleForm(false)}>
              &times;
            </button>
            <div className="p-8 text-gray-200">
              <h1 className="text-3xl font-bold mb-6">Создание статьи</h1>
              <form onSubmit={handleArticleSubmit}>
                <div className="mb-6">
                  <label htmlFor="articleTitle" className="block text-gray-300 font-medium mb-2">
                    Заголовок
                  </label>
                  <input
                    type="text"
                    id="articleTitle"
                    className="w-full px-4 py-3 rounded-lg border border-gray-600 bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={articleTitle}
                    onChange={(e) => setArticleTitle(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-6">
                  <label htmlFor="articleSubtitle" className="block text-gray-300 font-medium mb-2">
                    Подзаголовок
                  </label>
                  <input
                    type="text"
                    id="articleSubtitle"
                    className="w-full px-4 py-3 rounded-lg border border-gray-600 bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={articleSubtitle}
                    onChange={(e) => setArticleSubtitle(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-8">
                  <label htmlFor="articleContent" className="block text-gray-300 font-medium mb-2">
                    О себе
                  </label>
                  <textarea
                    id="articleContent"
                    className="content-field w-full px-4 py-3 rounded-lg border border-gray-600 bg-gray-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={articleContent}
                    onChange={(e) => setArticleContent(e.target.value)}
                  />
                </div>
                <div className="mb-8">
                  <h3 className="text-xl font-semibold text-gray-200 mb-4">Выберите ваши интересы (до 5)</h3>
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                    {tagOptions.map((tag, idx) => (
                      <div className="flex items-center" key={tag.value}>
                        <input
                          type="checkbox"
                          id={`tag${idx}`}
                          className="hidden tag-input"
                          checked={articleTags.includes(tag.value)}
                          onChange={() => handleTagChange(tag.value)}
                        />
                        <label
                          htmlFor={`tag${idx}`}
                          className="tag-label cursor-pointer px-4 py-2 border border-gray-600 rounded-full text-sm font-medium hover:bg-gray-700 transition"
                        >
                          <i className={`${tag.icon} mr-2`} />
                          {tag.value}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
                <button
                  type="submit"
                  className="w-full bg-gray-600 hover:bg-gray-500 text-white font-bold py-3 px-4 rounded-lg transition duration-300 transform hover:scale-105"
                >
                  Создать статью
                </button>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Profile
