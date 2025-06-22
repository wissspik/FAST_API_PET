import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import './Feed.css'

function Dashboard() {
  const [showCash, setShowCash] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    const checkAuth = async () => {
      const res = await fetch('http://localhost:8000/protected', {
        credentials: 'include',
      })
      if (!res.ok) {
        navigate('/login')
      }
    }
    checkAuth()
  }, [navigate])

  const handleClick = () => {
    setShowCash(true)
  }

  return (
    <div className="feed-page">
      <button className="cash-button" onClick={handleClick}>
        Сделать кэшик
      </button>
      {showCash && <div className="cash-display">💵💵💵</div>}
    </div>
  )
}

export default Dashboard
