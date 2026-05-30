import { Link, useLocation } from 'react-router-dom'
import { LayoutDashboard, BookOpen, HelpCircle, Github } from 'lucide-react'
const links = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/topics', label: 'Topics', icon: BookOpen },
  { path: '/quiz', label: 'Quiz', icon: HelpCircle },
]
export default function Sidebar() {
  const loc = useLocation()
  return (
    <aside className="fixed left-0 top-0 bottom-0 w-60 bg-void border-r border-[#333] flex flex-col p-4">
      <Link to="/" className="text-lg font-bold text-amber mb-8 px-2">🌐 NetworkOps</Link>
      <nav className="flex-1 space-y-1">
        {links.map(({path,label,icon:I}) => <Link key={path} to={path} className={loc.pathname===path?'nav-active':'nav-item'}><I className="w-4 h-4"/>{label}</Link>)}
      </nav>
      <div className="border-t border-[#333] pt-4">
        <a href="https://github.com/Yash-Patil-1" target="_blank" className="nav-item"><Github className="w-4 h-4"/>GitHub</a>
      </div>
    </aside>
  )
}
