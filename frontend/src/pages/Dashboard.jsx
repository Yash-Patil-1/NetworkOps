import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { BookOpen, HelpCircle, ArrowRight } from 'lucide-react'
import axios from 'axios'

export default function Dashboard() {
  const [stats, setStats] = useState({})
  useEffect(() => {
    Promise.all([axios.get('/api/topics?limit=1'), axios.get('/api/quiz/stats'), axios.get('/api/domains')])
      .then(([t, q, d]) => setStats({ topics: t.data.total, quizAcc: q.data.accuracy, domains: d.data.domains.length }))
      .catch(() => {})
  }, [])

  return (
    <div className="max-w-5xl">
      <h1 className="text-4xl font-bold mb-2">NetworkOps</h1>
      <p className="text-ash text-lg mb-10">Learn networking — fundamentals to automation. Theory + Quiz.</p>
      <div className="grid grid-cols-3 gap-4 mb-12">
        <div className="card text-center py-6"><BookOpen className="w-6 h-6 text-amber mx-auto mb-2"/><span className="text-2xl font-bold">{stats.topics||'—'}</span><p className="text-xs text-ash mt-1">Topics</p></div>
        <div className="card text-center py-6"><HelpCircle className="w-6 h-6 text-green mx-auto mb-2"/><span className="text-2xl font-bold">{stats.quizAcc||0}%</span><p className="text-xs text-ash mt-1">Quiz Accuracy</p></div>
        <div className="card text-center py-6"><span className="text-2xl font-bold">{stats.domains||'—'}</span><p className="text-xs text-ash mt-1">Domains</p></div>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <Link to="/topics" className="card group flex justify-between items-center hover:border-amber/30"><div><h3 className="font-medium">Browse Topics</h3><p className="text-xs text-ash">Theory with why/how/when</p></div><ArrowRight className="w-4 h-4 text-ash group-hover:text-amber"/></Link>
        <Link to="/quiz" className="card group flex justify-between items-center hover:border-amber/30"><div><h3 className="font-medium">Take Quiz</h3><p className="text-xs text-ash">Command, scenario & theory questions</p></div><ArrowRight className="w-4 h-4 text-ash group-hover:text-amber"/></Link>
      </div>
    </div>
  )
}
