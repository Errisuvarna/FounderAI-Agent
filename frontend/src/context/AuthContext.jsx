import { createContext, useContext, useEffect, useState } from 'react'
import { loginUser, registerUser, fetchProfile } from '../api/founderApi'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const bootstrapSession = async () => {
      const token = localStorage.getItem('founderai_access_token')
      const cachedUser = localStorage.getItem('founderai_user')

      if (!token) {
        setIsLoading(false)
        return
      }

      if (cachedUser) {
        setUser(JSON.parse(cachedUser))
      }

      try {
        const profile = await fetchProfile()
        setUser(profile)
        localStorage.setItem('founderai_user', JSON.stringify(profile))
      } catch {
        // Interceptor already handles 401 redirects/cleanup.
      } finally {
        setIsLoading(false)
      }
    }

    bootstrapSession()
  }, [])

  const persistSession = (data) => {
    localStorage.setItem('founderai_access_token', data.access_token)
    localStorage.setItem('founderai_refresh_token', data.refresh_token)
    localStorage.setItem('founderai_user', JSON.stringify(data.user))
    setUser(data.user)
  }

  const login = async (credentials) => {
    const data = await loginUser(credentials)
    persistSession(data)
    return data
  }

  const register = async (details) => {
    const data = await registerUser(details)
    persistSession(data)
    return data
  }

  const logout = () => {
    localStorage.removeItem('founderai_access_token')
    localStorage.removeItem('founderai_refresh_token')
    localStorage.removeItem('founderai_user')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
