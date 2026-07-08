import ReactMarkdown from 'react-markdown'

export default function BlueprintCard({ icon, tag, title, markdown, accent = 'blueprint' }) {
  const accentClasses =
    accent === 'stamp'
      ? 'bg-stamp-500/10 text-stamp-500'
      : 'bg-blueprint-500/10 text-blueprint-500'

  return (
    <section className="panel corner-marks p-7">
      <div className="flex items-center gap-3 mb-5">
        <span className={`w-9 h-9 rounded-md flex items-center justify-center shrink-0 ${accentClasses}`}>
          {icon}
        </span>
        <div>
          <p className="label-tag">{tag}</p>
          <h2 className="font-display font-semibold text-lg leading-tight">{title}</h2>
        </div>
      </div>
      <div className="prose-blueprint">
        <ReactMarkdown>{markdown || '_No output generated for this section._'}</ReactMarkdown>
      </div>
    </section>
  )
}
