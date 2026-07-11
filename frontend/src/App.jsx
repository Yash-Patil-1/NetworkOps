import { useState, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Topics from './pages/Topics'
import TopicDetail from './pages/TopicDetail'
import Quiz from './pages/Quiz'
import Learn from './pages/Learn'
import LessonView from './pages/LessonView'

export default function App() {
  const [lightMode, setLightMode] = useState(() => localStorage.getItem('netops-theme') === 'light')
  useEffect(() => {
    document.documentElement.classList.toggle('light', lightMode)
    localStorage.setItem('netops-theme', lightMode ? 'light' : 'dark')
  }, [lightMode])
  const toggleLightMode = () => setLightMode(prev => !prev)

  return (
    <div className="flex min-h-screen">
      <Sidebar lightMode={lightMode} toggleLightMode={toggleLightMode} />
      <main className="flex-1 ml-60 p-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/learn" element={<Learn />} />
          <Route path="/learn/:id" element={<LessonView />} />
          <Route path="/topics" element={<Topics />} />
          <Route path="/topics/:id" element={<TopicDetail />} />
          <Route path="/quiz" element={<Quiz />} />
        </Routes>
      </main>
    </div>
  )
}
