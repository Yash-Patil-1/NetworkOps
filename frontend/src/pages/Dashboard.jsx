import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { HelpCircle, ArrowRight, Zap, Flame, GraduationCap, TrendingUp } from 'lucide-react'
import axios from 'axios'

export default function Dashboard() {
  const [stats, setStats] = useState({})
  const [streak, setStreak] = useState(null)

  useEffect(() => {
    Promise.all([
      axios.get('/api/topics?limit=1'),
      axios.get('/api/quiz/stats'),
      axios.get('/api/domains'),
      axios.get('/api/progress'),
      axios.get('/api/streak'),
    ]).then(([t, q, d, p, s]) => {
      setStats({
        topics: t.data.total,
        quizAcc: q.data.accuracy,
        domains: d.data.domains.length,
        learned: p.data.learned,
        total: p.data.total_topics,
        progressPct: p.data.percentage,
      })
      setStreak(s.data)
    }).catch(() => {})
  }, [])

  const progressPct = stats.progressPct || 0
  const circumference = 2 * Math.PI * 36 // r=36
  const strokeDashoffset = circumference - (progressPct / 100) * circumference

  return (
    <div className="max-w-6xl">
      <h1 className="text-3xl font-bold text-chalk mb-1">NetworkOps</h1>
      <p className="text-cool-ash text-sm mb-8 font-mono tracking-wide">
        NETWORK ENGINEERING · NOC OPERATIONS · AUTOMATION
      </p>

      {/* Top row: Tachometer + XP strip */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        {/* Tachometer completion ring */}
        <div className="card flex flex-col items-center justify-center py-5 col-span-1">
          <div className="relative w-24 h-24 mb-2">
            <svg className="w-24 h-24 -rotate-90" viewBox="0 0 80 80">
              {/* Background ring */}
              <circle cx="40" cy="40" r="36" fill="none" stroke="var(--color-carbon-panel)" strokeWidth="4" />
              {/* Progress arc - red needle */}
              <circle cx="40" cy="40" r="36" fill="none" stroke="var(--color-guards-red)" strokeWidth="4"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round" />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-lg font-bold font-mono text-chalk">{progressPct}%</span>
              <span className="text-[8px] text-cool-ash font-mono tracking-wider uppercase">Learned</span>
            </div>
          </div>
          <span className="text-[10px] text-cool-ash font-mono">
            {stats.learned || 0} / {stats.total || 0} topics
          </span>
        </div>

        {/* XP Today */}
        <div className="card flex items-center gap-4 py-5">
          <div className="w-10 h-10 rounded-full bg-red/10 border border-red/20 flex items-center justify-center">
            <Zap className="w-5 h-5 text-red" />
          </div>
          <div>
            <p className="text-lg font-bold font-mono text-chalk">{streak?.today_xp || 0} / {streak?.daily_goal || 50}</p>
            <p className="text-[10px] text-cool-ash font-mono tracking-wide uppercase">XP Today</p>
            {/* Tiny bar */}
            <div className="w-24 h-1 bg-carbon mt-1 rounded-full overflow-hidden">
              <div className="h-full bg-red rounded-full transition-all"
                style={{ width: `${Math.min(100, ((streak?.today_xp || 0) / (streak?.daily_goal || 50)) * 100)}%` }} />
            </div>
          </div>
        </div>

        {/* Streak flame */}
        <div className="card flex items-center gap-4 py-5">
          <div className={`w-10 h-10 rounded-full border flex items-center justify-center ${(streak?.goal_met || streak?.current_streak > 0) ? 'bg-red/10 border-red/20' : 'bg-carbon/30 border-carbon'}`}>
            <Flame className={`w-5 h-5 ${(streak?.goal_met || streak?.current_streak > 0) ? 'text-red' : 'text-cool-ash'}`} />
          </div>
          <div>
            <p className="text-lg font-bold font-mono text-chalk">{streak?.current_streak || 0} days</p>
            <p className="text-[10px] text-cool-ash font-mono tracking-wide uppercase">Current Streak</p>
          </div>
        </div>

        {/* Level */}
        <div className="card flex items-center gap-4 py-5">
          <div className="w-10 h-10 rounded-full bg-green/10 border border-green/20 flex items-center justify-center">
            <TrendingUp className="w-5 h-5 text-green" />
          </div>
          <div>
            <p className="text-lg font-bold font-mono text-chalk">LVL {streak?.level || 1}</p>
            <p className="text-[10px] text-cool-ash font-mono tracking-wide uppercase">{streak?.total_xp || 0} Total XP</p>
          </div>
        </div>
      </div>

      {/* 7-day week strip */}
      {streak?.last_7_days && (
        <div className="card mb-8 py-3 px-4 flex items-center justify-between">
          <span className="text-[10px] text-cool-ash font-mono tracking-wider uppercase mr-4">Week</span>
          <div className="flex gap-3">
            {streak.last_7_days.map((day, i) => {
              const dayName = ['Su','Mo','Tu','We','Th','Fr','Sa'][new Date(day.date).getDay()]
              const isFilled = day.xp >= (streak.daily_goal || 50)
              const isPartial = day.xp > 0 && !isFilled
              return (
                <div key={i} className="flex flex-col items-center gap-1">
                  <div className={`w-6 h-6 rounded-full flex items-center justify-center
                    ${isFilled ? 'bg-red border border-red/30' : isPartial ? 'bg-red/20 border border-red/10' : 'bg-carbon border border-carbon/50'}`}>
                    <span className={`text-[9px] font-mono font-bold ${isFilled ? 'text-chalk-white' : isPartial ? 'text-red' : 'text-cool-ash'}`}>
                      {day.xp}
                    </span>
                  </div>
                  <span className="text-[8px] text-cool-ash font-mono">{dayName}</span>
                </div>
              )
            })}
          </div>
          <div className="flex items-center gap-2 ml-4">
            <span className={`w-2 h-2 rounded-full ${(streak?.goal_met) ? 'bg-green' : 'bg-carbon'}`} />
            <span className="text-[10px] text-cool-ash font-mono">{streak?.goal_met ? 'Goal Met' : 'Goal: 50 XP'}</span>
          </div>
        </div>
      )}

      {/* Interface-status style stats row */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <div className="card flex items-center gap-3 py-4">
          <span className="w-2 h-2 rounded-full bg-green"></span>
          <div>
            <span className="text-lg font-bold font-mono text-chalk">{stats.topics || '—'}</span>
            <p className="text-[9px] text-cool-ash font-mono tracking-wider uppercase">Topics</p>
          </div>
        </div>
        <div className="card flex items-center gap-3 py-4">
          <span className={`w-2 h-2 rounded-full ${(stats.quizAcc || 0) >= 70 ? 'bg-green' : (stats.quizAcc || 0) >= 40 ? 'bg-warn' : 'bg-down'}`}></span>
          <div>
            <span className="text-lg font-bold font-mono text-chalk">{stats.quizAcc || 0}%</span>
            <p className="text-[9px] text-cool-ash font-mono tracking-wider uppercase">Quiz Accuracy</p>
          </div>
        </div>
        <div className="card flex items-center gap-3 py-4">
          <span className="w-2 h-2 rounded-full bg-green"></span>
          <div>
            <span className="text-lg font-bold font-mono text-chalk">{stats.domains || '—'}</span>
            <p className="text-[9px] text-cool-ash font-mono tracking-wider uppercase">Domains</p>
          </div>
        </div>
        <div className="card flex items-center gap-3 py-4">
          <span className="w-2 h-2 rounded-full bg-green"></span>
          <div>
            <span className="text-lg font-bold font-mono text-chalk">{streak?.longest_streak || 0}</span>
            <p className="text-[9px] text-cool-ash font-mono tracking-wider uppercase">Best Streak</p>
          </div>
        </div>
      </div>

      {/* Quick links */}
      <div className="grid grid-cols-2 gap-4">
        <Link to="/learn" className="card group flex justify-between items-center hover:border-red/30 transition-colors cursor-pointer">
          <div className="flex items-center gap-3">
            <GraduationCap className="w-4 h-4 text-red" />
            <div>
              <h3 className="font-medium text-sm text-chalk">Guided Lessons</h3>
              <p className="text-[10px] text-cool-ash font-mono">Structured theory with checkpoints</p>
            </div>
          </div>
          <ArrowRight className="w-4 h-4 text-cool-ash group-hover:text-red transition-colors" />
        </Link>
        <Link to="/quiz" className="card group flex justify-between items-center hover:border-red/30 transition-colors cursor-pointer">
          <div className="flex items-center gap-3">
            <HelpCircle className="w-4 h-4 text-red" />
            <div>
              <h3 className="font-medium text-sm text-chalk">Take Quiz</h3>
              <p className="text-[10px] text-cool-ash font-mono">Command, scenario & theory questions</p>
            </div>
          </div>
          <ArrowRight className="w-4 h-4 text-cool-ash group-hover:text-red transition-colors" />
        </Link>
      </div>
    </div>
  )
}
