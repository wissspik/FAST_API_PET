import { useState } from 'react'
import './Feed.css'

function Feed() {
  const [showCash, setShowCash] = useState(false)

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

export default Feed
