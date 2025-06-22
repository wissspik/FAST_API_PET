import avatar from './assets/react.svg'
import './Feed.css'

function Feed() {
  const menuItems = [
    'Профиль',
    'Лента',
    'Мессенджер',
    'Звонки',
    'Друзья',
    'Сообщества',
    'Фото',
    'Музыка',
    'Видео',
    'Игры',
    'Маркет',
    'Файлы',
    'Помощь',
  ]

  return (
    <div className="feed-page">
      <aside className="sidebar">
        <nav>
          <ul className="menu">
            {menuItems.map((item) => (
              <li key={item} className="menu-item">
                <span className="icon">📁</span>
                <span className="label">{item}</span>
              </li>
            ))}
          </ul>
        </nav>
      </aside>
      <main className="main-area">
        <header className="profile-header">
          <div className="profile-block">
            <img src={avatar} alt="avatar" className="avatar" />
            <span className="name">Имя Пользователя</span>
            <span className="arrow">▼</span>
          </div>
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
