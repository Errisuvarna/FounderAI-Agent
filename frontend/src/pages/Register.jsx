import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Compass, ArrowRight, AlertCircle } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (form.password.length < 8) {
      setError('Password must be at least 8 characters long.')
      return
    }

    setIsSubmitting(true)
    try {
      await register(form)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Unable to create your account. Try a different email.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen grid-surface bg-ink-900 flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        <div className="flex items-center gap-2 justify-center mb-8">
          <Compass className="w-6 h-6 text-blueprint-500" />
          <span className="font-display font-semibold text-xl">
            Founder<span className="text-blueprint-500">AI</span>
          </span>
        </div>

        <div className="panel corner-marks p-8">
          <p className="label-tag mb-2">Session / Register</p>
          <h1 className="text-2xl font-semibold mb-6">Draft your first blueprint</h1>

          {error && (
            <div className="flex items-start gap-2 bg-danger-500/10 border border-danger-500/30 text-danger-500 text-sm rounded-md px-3 py-2 mb-4">
              <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label-tag block mb-1.5" htmlFor="name">Full name</label>
              <input
                id="name"
                name="name"
                type="text"
                required
                minLength={2}
                className="input-field"
                placeholder="Ada Lovelace"
                value={form.name}
                onChange={handleChange}
              />
            </div>
            <div>
              <label className="label-tag block mb-1.5" htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="input-field"
                placeholder="you@startup.com"
                value={form.email}
                onChange={handleChange}
              />
            </div>
            <div>
              <label className="label-tag block mb-1.5" htmlFor="password">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                required
                minLength={8}
                className="input-field"
                placeholder="At least 8 characters"
                value={form.password}
                onChange={handleChange}
              />
            </div>
            <button type="submit" disabled={isSubmitting} className="btn-primary w-full mt-2">
              {isSubmitting ? 'Creating account…' : 'Create account'}
              {!isSubmitting && <ArrowRight className="w-4 h-4" />}
            </button>
          </form>
        </div>

        <p className="text-center text-sm text-paper-500 mt-6">
          Already have an account?{' '}
          <Link to="/login" className="text-blueprint-500 hover:text-blueprint-400">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  )
}
