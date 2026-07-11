import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Search, Network, Shield, Cloud, Terminal, Monitor, Cpu } from 'lucide-react'
import axios from 'axios'

const DOMAIN_META = {
  fundamentals: { label: 'Networking Fundamentals', icon: Cpu, color: 'text-blue-400' },
  network_engineering: { label: 'Network Engineering', icon: Network, color: 'text-amber-400' },
  noc_operations: { label: 'NOC Operations', icon: Monitor, color: 'text-green-400' },
  network_security: { label: 'Network Security', icon: Shield, color: 'text-red-400' },
  cloud_networking: { label: 'Cloud Networking', icon: Cloud, color: 'text-purple-400' },
  network_automation: { label: 'Network Automation', icon: Terminal, color: 'text-cyan-400' },
}

export default function Topics() {
  const [topics, setTopics] = useState([])
  const [search, setSearch] = useState('')
  const [activeDomain, setActiveDomain] = useState(null)

  useEffect(() => {
    if (search.length >= 2) {
      axios.get(`/api/topics/search?q=${search}`).then(r => setTopics(r.data.topics))
    } else if (activeDomain) {
      axios.get(`/api/topics?domain=${activeDomain}&limit=100`).then(r => setTopics(r.data.topics))
    } else {
      axios.get('/api/topics?limit=200').then(r => setTopics(r.data.topics))
    }
  }, [search, activeDomain])

  // Group topics by domain
  const grouped = {}
  topics.forEach(t => {
    const d = t.domain || 'other'
    if (!grouped[d]) grouped[d] = []
    grouped[d].push(t)
  })

  return (
    <div className="max-w-5xl">
      <h1 className="text-3xl font-bold mb-2">Topics</h1>
      <p className="text-ash mb-6">150 topics across 6 networking domains</p>

      {/* Search */}
      <div className="relative mb-6">
        <Search className="absolute left-3 top-3 w-4 h-4 text-ash" />
        <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search topics..." className="input-field pl-10" />
      </div>

      {/* Domain filter tabs */}
      <div className="flex flex-wrap gap-2 mb-8">
        <button onClick={() => setActiveDomain(null)}
          className={`px-3 py-1.5 rounded text-xs font-medium transition ${!activeDomain ? 'bg-red/20 text-red border border-red/50' : 'bg-white/5 text-ash hover:text-chalk border border-carbon/30 hover:border-red/30'}`}>
          All Domains
        </button>
        {Object.entries(DOMAIN_META).map(([key, { label }]) => (
          <button key={key} onClick={() => setActiveDomain(key)}
            className={`px-3 py-1.5 rounded text-xs font-medium transition ${activeDomain === key ? 'bg-red/20 text-red border border-red/50' : 'bg-white/5 text-ash hover:text-chalk border border-carbon/30 hover:border-red/30'}`}>
            {label}
          </button>
        ))}
      </div>

      {/* Topics grouped by domain */}
      {Object.entries(grouped).map(([domain, domainTopics]) => {
        const meta = DOMAIN_META[domain] || { label: domain, icon: Cpu, color: 'text-ash' }
        const Icon = meta.icon
        return (
          <div key={domain} className="mb-8">
            <div className="flex items-center gap-2 mb-3">
              <Icon className={`w-5 h-5 ${meta.color}`} />
              <h2 className="text-lg font-semibold text-chalk">{meta.label}</h2>
              <span className="text-xs text-ash ml-2">({domainTopics.length} topics)</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {domainTopics.map(t => (
                <Link key={t.id} to={`/topics/${t.id}`} className="card block hover:border-red/30 transition-colors">
                  <div className="flex justify-between items-center">
                    <h3 className="font-medium text-sm text-chalk">{t.name}</h3>
                    <div className="flex gap-2">
                      {t.difficulty && <span className="tag-red">{t.difficulty}</span>}
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )
      })}

      {topics.length === 0 && (
        <p className="text-ash text-center py-8">No topics found.</p>
      )}
    </div>
  )
}
