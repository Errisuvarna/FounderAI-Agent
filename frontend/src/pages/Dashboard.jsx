import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Rocket, FileText, ArrowRight, Users, LineChart, Cpu } from 'lucide-react'
import Navbar from '../components/Navbar'
import { useAuth } from '../context/AuthContext'

export default function Dashboard() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [lastBlueprint, setLastBlueprint] = useState(null)

  useEffect(() => {
    const cached = localStorage.getItem('founderai_last_blueprint')
    if (cached) {
      try {
        setLastBlueprint(JSON.parse(cached))
      } catch {
        setLastBlueprint(null)
      }
    }
  }, [])

  const firstName = user?.name?.split(' ')[0] || 'Founder'

  return (
    <div className="min-h-screen bg-ink-900 grid-surface">
      <Navbar />

      <main className="max-w-6xl mx-auto px-6 py-14">
        <p className="label-tag mb-3">Dashboard / {firstName}</p>
        <h1 className="text-3xl sm:text-4xl font-semibold mb-3 max-w-2xl">
          Turn today&apos;s idea into a fundable blueprint.
        </h1>
        <p className="text-paper-500 max-w-xl mb-10">
          Five specialized AI agents — market research, finance, tech architecture, growth
          strategy, and pitch writing — collaborate in sequence to draft your startup plan.
        </p>

        <div className="grid md:grid-cols-3 gap-5 mb-12">
          <FeatureCard
            icon={<Users className="w-5 h-5" />}
            title="5 collaborating agents"
            description="Each agent specializes in one discipline and builds on the last agent's findings."
          />
          <FeatureCard
            icon={<LineChart className="w-5 h-5" />}
            title="Real calculations"
            description="Unit economics and revenue projections run through an actual financial calculator, not guesses."
          />
          <FeatureCard
            icon={<Cpu className="w-5 h-5" />}
            title="Grounded in research"
            description="Live web search and a retrieval-augmented knowledge base back every major claim."
          />
        </div>

        <div className="grid sm:grid-cols-2 gap-5">
          <button
            onClick={() => navigate('/generate')}
            className="panel corner-marks p-7 text-left group hover:border-blueprint-500/50 transition-colors"
          >
            <div className="flex items-center justify-between mb-4">
              <span className="w-10 h-10 rounded-md bg-blueprint-500/10 flex items-center justify-center text-blueprint-500">
                <Rocket className="w-5 h-5" />
              </span>
              <ArrowRight className="w-4 h-4 text-paper-500 group-hover:text-blueprint-500 group-hover:translate-x-1 transition-all" />
            </div>
            <h2 className="font-display font-semibold text-lg mb-1.5">Generate a new blueprint</h2>
            <p className="text-sm text-paper-500">
              Describe your idea and let the crew draft a complete business plan.
            </p>
          </button>

          <button
            onClick={() => lastBlueprint && navigate('/result')}
            disabled={!lastBlueprint}
            className="panel corner-marks p-7 text-left group hover:border-blueprint-500/50 transition-colors disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:border-ink-600"
          >
            <div className="flex items-center justify-between mb-4">
              <span className="w-10 h-10 rounded-md bg-stamp-500/10 flex items-center justify-center text-stamp-500">
                <FileText className="w-5 h-5" />
              </span>
              {lastBlueprint && (
                <ArrowRight className="w-4 h-4 text-paper-500 group-hover:text-stamp-500 group-hover:translate-x-1 transition-all" />
              )}
            </div>
            <h2 className="font-display font-semibold text-lg mb-1.5">
              {lastBlueprint ? lastBlueprint.idea_title : 'No blueprint yet'}
            </h2>
            <p className="text-sm text-paper-500">
              {lastBlueprint
                ? 'Reopen your most recently generated blueprint.'
                : 'Your most recent blueprint will appear here once generated.'}
            </p>
          </button>
        </div>
      </main>
    </div>
  )
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="panel p-5">
      <span className="w-9 h-9 rounded-md bg-ink-700 flex items-center justify-center text-blueprint-500 mb-3">
        {icon}
      </span>
      <h3 className="font-display font-medium mb-1">{title}</h3>
      <p className="text-sm text-paper-500">{description}</p>
    </div>
  )
}
