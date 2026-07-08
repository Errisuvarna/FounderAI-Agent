import { useEffect, useState } from 'react'
import { Check, Search, Calculator, Cpu, TrendingUp, PenTool } from 'lucide-react'

const AGENTS = [
  {
    key: 'market_research',
    name: 'Market Research Agent',
    detail: 'Sizing the market and scanning competitors',
    icon: Search,
    estimateMs: 9000,
  },
  {
    key: 'finance',
    name: 'Finance Agent',
    detail: 'Modeling unit economics and revenue projections',
    icon: Calculator,
    estimateMs: 8000,
  },
  {
    key: 'tech_architect',
    name: 'Tech Architect Agent',
    detail: 'Drafting the MVP stack and system design',
    icon: Cpu,
    estimateMs: 8000,
  },
  {
    key: 'strategy',
    name: 'Strategy Agent',
    detail: 'Defining go-to-market and growth roadmap',
    icon: TrendingUp,
    estimateMs: 8000,
  },
  {
    key: 'pitch_writer',
    name: 'Pitch Writer Agent',
    detail: 'Synthesizing the executive summary and pitch deck',
    icon: PenTool,
    estimateMs: 7000,
  },
]

/**
 * Staged progress UI. The backend runs the crew as one blocking call, so
 * this component estimates per-agent timing client-side to give visible
 * feedback while the real request is in flight. It never claims "done"
 * until `isComplete` is actually true.
 */
export default function AgentProgressTracker({ isComplete }) {
  const [activeIndex, setActiveIndex] = useState(0)

  useEffect(() => {
    if (isComplete || activeIndex >= AGENTS.length - 1) return
    const timer = setTimeout(() => {
      setActiveIndex((prev) => Math.min(prev + 1, AGENTS.length - 1))
    }, AGENTS[activeIndex].estimateMs)
    return () => clearTimeout(timer)
  }, [activeIndex, isComplete])

  return (
    <div className="panel corner-marks p-8 max-w-lg w-full">
      <p className="label-tag mb-1">Crew execution / live</p>
      <h2 className="text-xl font-semibold mb-6">Drafting your blueprint…</h2>

      <ol className="space-y-5">
        {AGENTS.map((agent, index) => {
          const status = isComplete
            ? 'done'
            : index < activeIndex
              ? 'done'
              : index === activeIndex
                ? 'active'
                : 'pending'
          const Icon = agent.icon

          return (
            <li key={agent.key} className="flex items-start gap-4">
              <div
                className={`w-9 h-9 rounded-md flex items-center justify-center shrink-0 border transition-colors ${
                  status === 'done'
                    ? 'bg-blueprint-500/15 border-blueprint-500 text-blueprint-500'
                    : status === 'active'
                      ? 'bg-stamp-500/10 border-stamp-500 text-stamp-500 animate-pulseDot'
                      : 'bg-ink-800 border-ink-600 text-paper-500'
                }`}
              >
                {status === 'done' ? <Check className="w-4 h-4" /> : <Icon className="w-4 h-4" />}
              </div>
              <div className="flex-1">
                <p
                  className={`font-mono text-[11px] uppercase tracking-wider mb-0.5 ${
                    status === 'pending' ? 'text-paper-500' : 'text-blueprint-500'
                  }`}
                >
                  Agent {String(index + 1).padStart(2, '0')} / 05
                </p>
                <p className={`font-medium ${status === 'pending' ? 'text-paper-500' : 'text-paper-100'}`}>
                  {agent.name}
                </p>
                {status === 'active' && (
                  <p className="text-sm text-paper-500 mt-0.5">{agent.detail}</p>
                )}
              </div>
            </li>
          )
        })}
      </ol>

      <p className="text-xs text-paper-500 mt-7 border-t border-ink-600 pt-4">
        This typically takes 30–90 seconds depending on model and search latency.
      </p>
    </div>
  )
}
