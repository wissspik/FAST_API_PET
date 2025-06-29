import { Link } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <div className="home">
      <h1>Welcome</h1>
      <div className="nav">
        <Link className="nav-link" to="/login">Login</Link>
        <Link className="nav-link" to="/registration">Registration</Link>
      </div>
    </div>
  )
}

export default App
