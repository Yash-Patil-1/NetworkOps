import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, BookOpen, HelpCircle, GraduationCap, Github } from 'lucide-react'
import StreakBadge from './StreakBadge'

const links = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/learn', label: 'Learn', icon: GraduationCap },
  { path: '/topics', label: 'Topics', icon: BookOpen },
  { path: '/quiz', label: 'Quiz', icon: HelpCircle },
]

export default function Sidebar() {
  const loc = useLocation()

  return (
    <aside className="fixed left-0 top-0 bottom-0 w-60 bg-graphite-black border-r border-carbon/50 flex flex-col p-4">
      <Link to="/" className="text-lg font-bold text-chalk mb-6 px-2 tracking-tight">
        <span className="text-red">⬡</span> NetworkOps
      </Link>

      <nav className="flex-1 space-y-0.5">
        {links.map(({path,label,icon:I}) => (
          <Link key={path} to={path}
            className={loc.pathname === path || (path !== '/' && loc.pathname.startsWith(path)) ? 'nav-active' : 'nav-item'}>
            <I className="w-4 h-4"/>{label}
          </Link>
        ))}
      </nav>

      <div className="space-y-2">
        <StreakBadge />
        <div className="border-t border-carbon/30 pt-3">
          <a href="https://github.com/Yash-Patil-1" target="_blank" className="nav-item">
            <Github className="w-4 h-4"/>GitHub
          </a>
        </div>
      </div>
    </aside>
  )
}
