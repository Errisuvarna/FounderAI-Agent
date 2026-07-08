import { Link, useNavigate } from 'react-router-dom'
import { Compass, LogOut } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="border-b border-ink-600 bg-ink-900/90 backdrop-blur sticky top-0 z-40">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link to="/dashboard" className="flex items-center gap-2 group">
          <Compass className="w-5 h-5 text-blueprint-500 group-hover:rotate-45 transition-transform duration-300" />
          <span className="font-display font-semibold text-lg tracking-tight">
            Founder<span className="text-blueprint-500">AI</span>
          </span>
        </Link>

        {user && (
          <div className="flex items-center gap-5">
            <div className="text-right hidden sm:block">
              <p className="text-sm text-paper-100 leading-tight">{user.name}</p>
              <p className="font-mono text-[11px] text-paper-500 leading-tight">{user.email}</p>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-1.5 text-sm text-paper-500 hover:text-danger-500 transition-colors"
            >
              <LogOut className="w-4 h-4" />
              Sign out
            </button>
          </div>
        )}
      </div>
    </header>
  )
}
