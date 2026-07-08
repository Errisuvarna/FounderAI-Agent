import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { AlertCircle, Sparkles } from 'lucide-react'
import Navbar from '../components/Navbar'
import AgentProgressTracker from '../components/AgentProgressTracker'
import { generateBlueprint } from '../api/founderApi'

const INITIAL_FORM = {
  idea_title: '',
  idea_description: '',
  industry: '',
  target_market: '',
}

export default function GenerateBlueprint() {
  const navigate = useNavigate()
  const [form, setForm] = useState(INITIAL_FORM)
  const [error, setError] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)
  const [isComplete, setIsComplete] = useState(false)

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setIsGenerating(true)
    setIsComplete(false)

    try {
      const blueprint = await generateBlueprint(form)
      setIsComplete(true)
      localStorage.setItem('founderai_last_blueprint', JSON.stringify(blueprint))
      // Brief pause so the tracker visibly reaches 100% before navigating.
      setTimeout(() => navigate('/result'), 600)
    } catch (err) {
      setIsGenerating(false)
      setError(
        err.response?.data?.detail ||
          'Blueprint generation failed. Check your backend and API keys, then try again.'
      )
    }
  }

  return (
    <div className="min-h-screen bg-ink-900 grid-surface">
      <Navbar />

      <main className="max-w-4xl mx-auto px-6 py-14">
        {!isGenerating ? (
          <>
            <p className="label-tag mb-3">New blueprint / Step 1 of 1</p>
            <h1 className="text-3xl font-semibold mb-2">Describe your startup idea</h1>
            <p className="text-paper-500 mb-10 max-w-xl">
              Be as specific as you can — the more context the agents have, the sharper the
              research, financials, and strategy will be.
            </p>

            {error && (
              <div className="flex items-start gap-2 bg-danger-500/10 border border-danger-500/30 text-danger-500 text-sm rounded-md px-4 py-3 mb-6">
                <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="panel corner-marks p-8 space-y-6">
              <div>
                <label className="label-tag block mb-1.5" htmlFor="idea_title">
                  Startup name / idea title
                </label>
                <input
                  id="idea_title"
                  name="idea_title"
                  required
                  minLength={3}
                  className="input-field"
                  placeholder="e.g. Fleetly — route optimization for local delivery fleets"
                  value={form.idea_title}
                  onChange={handleChange}
                />
              </div>

              <div>
                <label className="label-tag block mb-1.5" htmlFor="idea_description">
                  Idea description
                </label>
                <textarea
                  id="idea_description"
                  name="idea_description"
                  required
                  minLength={20}
                  rows={5}
                  className="input-field resize-none"
                  placeholder="What does it do, who is it for, and what problem does it solve?"
                  value={form.idea_description}
                  onChange={handleChange}
                />
              </div>

              <div className="grid sm:grid-cols-2 gap-6">
                <div>
                  <label className="label-tag block mb-1.5" htmlFor="industry">
                    Industry
                  </label>
                  <input
                    id="industry"
                    name="industry"
                    required
                    className="input-field"
                    placeholder="e.g. Logistics SaaS"
                    value={form.industry}
                    onChange={handleChange}
                  />
                </div>
                <div>
                  <label className="label-tag block mb-1.5" htmlFor="target_market">
                    Target market
                  </label>
                  <input
                    id="target_market"
                    name="target_market"
                    required
                    className="input-field"
                    placeholder="e.g. SMB delivery fleets in North America"
                    value={form.target_market}
                    onChange={handleChange}
                  />
                </div>
              </div>

              <button type="submit" className="btn-primary w-full sm:w-auto">
                <Sparkles className="w-4 h-4" />
                Generate blueprint
              </button>
            </form>
          </>
        ) : (
          <div className="flex flex-col items-center justify-center py-10">
            <AgentProgressTracker isComplete={isComplete} />
          </div>
        )}
      </main>
    </div>
  )
}
