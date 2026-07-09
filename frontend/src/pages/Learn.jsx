import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Search, BookOpen, ChevronRight, Network, Shield, Cloud, Terminal, Monitor, Cpu } from 'lucide-react'
import axios from 'axios'

const DOMAIN_META = {
  fundamentals: { label: 'Networking Fundamentals', icon: Cpu, color: 'text-blue-400' },
  network_engineering: { label: 'Network Engineering', icon: Network, color: 'text-red' },
  noc_operations: { label: 'NOC Operations', icon: Monitor, color: 'text-green' },
  network_security: { label: 'Network Security', icon: Shield, color: 'text-red' },
  cloud_networking: { label: 'Cloud Networking', icon: Cloud, color: 'text-purple-400' },
  network_automation: { label: 'Network Automation', icon: Terminal, color: 'text-cyan-400' },
}

export default function Learn() {
  const [lessons, setLessons] = useState([])
  const [search, setSearch] = useState('')
  const [activeDomain, setActiveDomain] = useState(null)
  useEffect(() => {
    axios.get('/api/lessons').then(r => setLessons(r.data.lessons || []))
  }, [])

  const filtered = lessons.filter(l => {
    if (search.length >= 2 && !l.title.toLowerCase().includes(search.toLowerCase()) && !l.id.includes(search.toLowerCase())) return false
    if (activeDomain && l.domain !== activeDomain) return false
    return true
  })

  const grouped = {}
  filtered.forEach(l => {
    const d = l.domain || 'other'
    if (!grouped[d]) grouped[d] = []
    grouped[d].push(l)
  })

  return (
    <div className="max-w-5xl">
      <h1 className="text-3xl font-bold mb-2">Guided Lessons</h1>
      <p className="text-ash mb-6">Learn networking with guided theory, active-recall checkpoints, and XP.</p>

      {/* Search */}
      <div className="relative mb-4">
        <Search className="absolute left-3 top-3 w-4 h-4 text-ash" />
        <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search lessons..." className="input-field pl-10" />
      </div>

      {/* Domain filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button onClick={() => setActiveDomain(null)}
          className={`px-3 py-1.5 rounded text-xs font-medium transition ${!activeDomain ? 'bg-red/20 text-red border border-red/50' : 'bg-white/5 text-ash hover:text-chalk border border-carbon/30'}`}>
          All Domains
        </button>
        {Object.entries(DOMAIN_META).map(([key, { label }]) => (
          <button key={key} onClick={() => setActiveDomain(key)}
            className={`px-3 py-1.5 rounded text-xs font-medium transition ${activeDomain === key ? 'bg-red/20 text-red border border-red/50' : 'bg-white/5 text-ash hover:text-chalk border border-carbon/30'}`}>
            {label}
          </button>
        ))}
      </div>

      {/* Lessons grouped by domain */}
      {Object.entries(grouped).map(([domain, domainLessons]) => {
        const meta = DOMAIN_META[domain] || { label: domain, icon: BookOpen, color: 'text-ash' }
        const Icon = meta.icon
        return (
          <div key={domain} className="mb-6">
            <div className="flex items-center gap-2 mb-3">
              <Icon className={`w-4 h-4 ${meta.color}`} />
              <h2 className="text-sm font-semibold text-chalk">{meta.label}</h2>
              <span className="text-[10px] text-ash font-mono">({domainLessons.length})</span>
            </div>
            <div className="space-y-1">
              {domainLessons.map(l => (
                <Link key={l.id} to={`/learn/${l.id}`}
                  className="card flex items-center justify-between py-3 px-4 group hover:border-red/40 transition-colors">
                  <div className="flex items-center gap-3 min-w-0">
                    <BookOpen className="w-4 h-4 text-ash shrink-0" />
                    <div className="min-w-0">
                      <h3 className="font-medium text-sm truncate">{l.title}</h3>
                      <div className="flex items-center gap-2 mt-0.5">
                        <span className="text-[10px] text-ash font-mono">{l.section_count} sections</span>
                        {l.checkpoint_count > 0 && (
                          <span className="text-[10px] text-green font-mono">{l.checkpoint_count} questions</span>
                        )}
                        {l.difficulty && (
                          <span className="text-[10px] text-ash font-mono">{l.difficulty}</span>
                        )}
                      </div>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-ash group-hover:text-red transition-colors shrink-0" />
                </Link>
              ))}
            </div>
          </div>
        )
      })}

      {filtered.length === 0 && (
        <p className="text-ash text-center py-8">No lessons found.</p>
      )}
    </div>
  )
}
