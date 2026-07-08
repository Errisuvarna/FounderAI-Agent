import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Calculator, Cpu, TrendingUp, Presentation, Rocket, Download } from 'lucide-react'
import Navbar from '../components/Navbar'
import BlueprintCard from '../components/BlueprintCard'

export default function ResultPage() {
  const navigate = useNavigate()
  const [blueprint, setBlueprint] = useState(null)

  useEffect(() => {
    const cached = localStorage.getItem('founderai_last_blueprint')
    if (cached) {
      setBlueprint(JSON.parse(cached))
    }
  }, [])

  if (!blueprint) {
    return (
      <div className="min-h-screen bg-ink-900 grid-surface">
        <Navbar />
        <main className="max-w-3xl mx-auto px-6 py-20 text-center">
          <p className="label-tag mb-3">No blueprint found</p>
          <h1 className="text-2xl font-semibold mb-6">Nothing to show yet</h1>
          <button onClick={() => navigate('/generate')} className="btn-primary">
            <Rocket className="w-4 h-4" />
            Generate a blueprint
          </button>
        </main>
      </div>
    )
  }

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(blueprint, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${blueprint.idea_title.replace(/\s+/g, '_').toLowerCase()}_blueprint.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="min-h-screen bg-ink-900 grid-surface">
      <Navbar />

      <main className="max-w-5xl mx-auto px-6 py-14">
        <div className="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4 mb-10">
          <div>
            <p className="label-tag mb-2">Blueprint / Complete</p>
            <h1 className="text-3xl font-semibold">{blueprint.idea_title}</h1>
          </div>
          <div className="flex gap-3">
            <button onClick={handleDownload} className="btn-secondary">
              <Download className="w-4 h-4" />
              Export JSON
            </button>
            <button onClick={() => navigate('/generate')} className="btn-primary">
              <Rocket className="w-4 h-4" />
              New blueprint
            </button>
          </div>
        </div>

        <section className="panel corner-marks p-7 mb-8 border-blueprint-500/30">
          <p className="label-tag mb-2">Executive Summary</p>
          <p className="text-paper-100 leading-relaxed">{blueprint.executive_summary}</p>
        </section>

        <div className="grid lg:grid-cols-2 gap-6">
          <BlueprintCard
            icon={<Search className="w-4 h-4" />}
            tag="Agent 01 — Market Research"
            title="Market Opportunity"
            markdown={blueprint.market_research?.markdown}
          />
          <BlueprintCard
            icon={<Calculator className="w-4 h-4" />}
            tag="Agent 02 — Finance"
            title="Financial Plan"
            markdown={blueprint.financial_plan?.markdown}
            accent="stamp"
          />
          <BlueprintCard
            icon={<Cpu className="w-4 h-4" />}
            tag="Agent 03 — Tech Architect"
            title="Technical Architecture"
            markdown={blueprint.tech_architecture?.markdown}
          />
          <BlueprintCard
            icon={<TrendingUp className="w-4 h-4" />}
            tag="Agent 04 — Strategy"
            title="Growth Strategy"
            markdown={blueprint.growth_strategy?.markdown}
            accent="stamp"
          />
        </div>

        <div className="mt-6">
          <BlueprintCard
            icon={<Presentation className="w-4 h-4" />}
            tag="Agent 05 — Pitch Writer"
            title="Pitch Deck Outline"
            markdown={blueprint.pitch_deck_outline?.markdown}
          />
        </div>
      </main>
    </div>
  )
}
