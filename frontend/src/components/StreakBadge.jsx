import { useEffect, useState } from 'react'
import { Flame } from 'lucide-react'
import axios from 'axios'

export default function StreakBadge() {
  const [data, setData] = useState(null)

  useEffect(() => {
    axios.get('/api/streak').then(r => setData(r.data)).catch(() => {})
    const interval = setInterval(() => {
      axios.get('/api/streak').then(r => setData(r.data)).catch(() => {})
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  if (!data) return null

  return (
    <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-black/20 border border-carbon/50">
      <div className={`flex items-center gap-1 ${data.goal_met ? 'text-red' : 'text-ash'}`}>
        <Flame className={`w-4 h-4 ${data.goal_met ? 'drop-shadow-[0_0_4px_rgba(213,0,28,0.5)]' : ''}`} />
        <span className="font-mono text-xs font-bold">{data.current_streak}</span>
      </div>
      <div className="text-[10px] leading-tight">
        <div className="text-ash font-mono">LVL {data.level}</div>
        <div className="text-chalk font-mono">{data.total_xp} XP</div>
      </div>
    </div>
  )
}
