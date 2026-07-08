import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import axios from 'axios'

export default function TopicDetail() {
  const { id } = useParams()
  const [topic, setTopic] = useState(null)
  useEffect(() => { axios.get(`/api/topics/${id}`).then(r => setTopic(r.data)) }, [id])
  if (!topic) return <p className="text-ash">Loading...</p>
  const t = topic.theory || {}

  return (
    <div className="max-w-4xl">
      <Link to="/topics" className="inline-flex items-center gap-1 text-ash hover:text-chalk text-sm mb-6"><ArrowLeft className="w-4 h-4"/>Back</Link>
      <h1 className="text-2xl font-bold mb-2">{topic.name}</h1>
      <div className="flex gap-2 mb-8"><span className="tag-red">{topic.domain?.replace(/_/g,' ')}</span><span className="tag-green">{topic.difficulty}</span></div>

      {t.what && <Section title="What" content={t.what}/>}
      {t.why && <Section title="Why" content={t.why}/>}
      {t.how && <Section title="How" content={t.how}/>}
      {t.when && <Section title="When" content={t.when}/>}
      {t.configuration && <div className="mb-6"><h2 className="text-sm font-bold text-red mb-2">Configuration</h2><pre className="bg-void border border-carbon rounded-lg p-4 text-xs font-mono text-chalk overflow-x-auto whitespace-pre-wrap">{t.configuration}</pre></div>}
      {t.troubleshooting && <div className="mb-6"><h2 className="text-sm font-bold text-red mb-2">Troubleshooting</h2><ul className="space-y-1">{t.troubleshooting.map((s,i)=><li key={i} className="text-xs text-ash font-mono">• {s}</li>)}</ul></div>}

      <Link to={`/quiz?topic=${topic.id}`} className="btn-primary mt-4">Take Quiz</Link>
    </div>
  )
}

function Section({title, content}) {
  return <div className="mb-6"><h2 className="text-sm font-bold text-red mb-2">{title}</h2><p className="text-sm text-ash leading-relaxed whitespace-pre-wrap">{content}</p></div>
}
