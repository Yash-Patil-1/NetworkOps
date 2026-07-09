import { useEffect, useState, useRef } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { ArrowLeft, CheckCircle, XCircle, Lightbulb, ChevronRight, BookOpen, Zap, Trophy, Flame } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import axios from 'axios'

export default function LessonView() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [lesson, setLesson] = useState(null)
  const [loading, setLoading] = useState(true)
  const [step, setStep] = useState(0) // which section we're on
  const [showCheckpoint, setShowCheckpoint] = useState(false)
  const [question, setQuestion] = useState(null)
  const [answer, setAnswer] = useState('')
  const [result, setResult] = useState(null)
  const [showHint, setShowHint] = useState(false)
  const [completed, setCompleted] = useState(false)
  const [xpEarned, setXpEarned] = useState(0)
  const [streak, setStreak] = useState(null)
  const [checkpointResults, setCheckpointResults] = useState([])
  const sectionRef = useRef(null)

  useEffect(() => {
    sectionRef.current?.focus()
  }, [step])

  useEffect(() => {
    setLoading(true)
    axios.get(`/api/lessons/${id}`).then(r => {
      setLesson(r.data)
      setLoading(false)
    }).catch(() => {
      setLoading(false)
      setLesson(null)
    })
  }, [id])

  const sections = lesson?.sections || []
  const qIds = lesson?.checkpoint_question_ids || []
  const totalSteps = sections.length + qIds.length // sections + checkpoints interleaved

  const advanceToNext = () => {
    setStep(s => s + 1)
    setShowCheckpoint(false)
    setQuestion(null)
    setAnswer('')
    setResult(null)
    setShowHint(false)
  }

  // Determine what to show at current step
  const sectionIdx = Math.floor(step / 2)
  const isCheckpoint = step % 2 === 1 && sectionIdx < sections.length && qIds.length > 0

  // Load checkpoint question when needed
  useEffect(() => {
    if (isCheckpoint && !question && !result) {
      const topicId = id
      axios.get(`/api/quiz/next?topic=${topicId}`).then(r => {
        setQuestion(r.data)
      }).catch(() => {
        // No questions available — skip checkpoint
        setShowCheckpoint(false)
        setQuestion(null)
      })
    }
  }, [isCheckpoint, question, result, id])

  const submitAnswer = () => {
    if (!answer.trim() || !question) return
    axios.post('/api/quiz/answer', { question_id: question.id, topic_id: id, answer })
      .then(r => {
        setResult(r.data)
        setCheckpointResults(prev => [...prev, { correct: r.data.correct, question: question.question }])
      })
  }

  const completeLesson = () => {
    axios.post(`/api/lessons/${id}/complete`).then(r => {
      setXpEarned(r.data.xp_awarded)
      setStreak({ current_streak: r.data.current_streak, level: r.data.level })
      setCompleted(true)
    }).catch(() => {
      setCompleted(true)
    })
  }

  // Handle keyboard submission
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      if (result) {
        advanceToNext()
      } else {
        submitAnswer()
      }
    }
  }

  if (loading) return <p className="text-ash">Loading lesson...</p>
  if (!lesson) return (
    <div className="max-w-3xl text-center py-16">
      <BookOpen className="w-12 h-12 text-ash mx-auto mb-4" />
      <h2 className="text-xl font-bold mb-2">Lesson Not Found</h2>
      <p className="text-ash mb-6">This topic may not have lesson content yet.</p>
      <Link to="/learn" className="btn-primary">Back to Lessons</Link>
    </div>
  )

  if (completed) {
    const correctCount = checkpointResults.filter(r => r.correct).length
    return (
      <div className="max-w-3xl mx-auto text-center py-12 animate-fade-in">
        <div className="mb-6">
          <Trophy className={`w-16 h-16 mx-auto mb-4 ${xpEarned > 0 ? 'text-red' : 'text-ash'}`} />
          <h2 className="text-2xl font-bold text-chalk mb-2">Lesson Complete!</h2>
          <p className="text-ash">{lesson.title}</p>
        </div>

        <div className="grid grid-cols-3 gap-3 mb-8">
          {xpEarned > 0 && (
            <div className="card py-4">
              <Zap className="w-5 h-5 text-red mx-auto mb-1" />
              <p className="text-lg font-bold text-chalk font-mono">+{xpEarned} XP</p>
              <p className="text-[10px] text-ash">Earned</p>
            </div>
          )}
          {streak && (
            <div className="card py-4">
              <Flame className="w-5 h-5 text-red mx-auto mb-1" />
              <p className="text-lg font-bold text-chalk font-mono">{streak.current_streak}</p>
              <p className="text-[10px] text-ash">Day Streak</p>
            </div>
          )}
          {checkpointResults.length > 0 && (
            <div className="card py-4">
              <p className="text-lg font-bold text-chalk font-mono">{correctCount}/{checkpointResults.length}</p>
              <p className="text-[10px] text-ash">Checkpoints Passed</p>
            </div>
          )}
          {streak && (
            <div className="card py-4">
              <p className="text-lg font-bold text-chalk font-mono">LVL {streak.level}</p>
              <p className="text-[10px] text-ash">Level</p>
            </div>
          )}
        </div>

        <div className="flex gap-3 justify-center">
          <Link to="/learn" className="btn-primary">More Lessons</Link>
          <Link to={`/quiz?topic=${id}`} className="btn-ghost">Take Topic Quiz</Link>
        </div>
      </div>
    )
  }

  // Show section content
  if (!isCheckpoint && sectionIdx < sections.length) {
    const section = sections[sectionIdx]
    const isLast = sectionIdx >= sections.length - 1
    const hasCheckpoints = qIds.length > 0
    const isLastStep = step >= (sections.length * 2) - 1

    return (
      <div ref={sectionRef} tabIndex={-1} className=" max-w-4xl animate-fade-in focus-visible:ring-1 focus-visible:ring-red outline-none">
        <Link to="/learn" className="inline-flex items-center  gap-1 text-ash hover:text-chalk text-sm mb-4">
          <ArrowLeft className="w-4 h-4" /> Back to Lessons
        </Link>

        <div className="flex items-center gap-3 mb-6">
          <div>
            <h1 className="text-xl font-bold text-chalk">{lesson.title}</h1>
            <p className="text-[10px] text-ash font-mono">
              {lesson.domain?.replace(/_/g, ' ')} · {lesson.difficulty}
            </p>
          </div>
        </div>

        {/* Progress bar */}
        <div className="flex gap-1 mb-6">
          {sections.map((s, i) => (
            <div key={i} className={`h-1 flex-1 rounded-full transition-colors ${
              i < sectionIdx ? 'bg-red' : i === sectionIdx ? 'bg-red/60' : 'bg-carbon'
            }`} />
          ))}
        </div>

        <div className="card mb-6 border-carbon/50">
          <h2 className="text-sm font-bold text-red mb-3 font-mono uppercase tracking-wider">
            {section.title}
          </h2>
          <div className="text-sm text-ash leading-relaxed [&_strong]:text-chalk [&_code]:text-red [&_code]:font-mono [&_code]:text-xs [&_code]:bg-red/5 [&_code]:px-1 [&_code]:rounded [&_pre]:bg-void [&_pre]:border [&_pre]:border-carbon [&_pre]:rounded-lg [&_pre]:p-3 [&_pre]:my-2 [&_pre]:text-xs [&_pre]:font-mono [&_pre]:text-chalk [&_pre]:overflow-x-auto [&_li]:text-ash [&_li]:text-sm [&_li]:ml-4 [&_p]:text-sm [&_p]:text-ash [&_p]:leading-relaxed [&_p]:mb-3">
              <ReactMarkdown>{section.content}</ReactMarkdown>
            </div>
        </div>

        {/* Key concepts */}
        {sectionIdx === 0 && lesson.key_concepts?.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-6">
            {lesson.key_concepts.map((c, i) => (
              <span key={i} className="px-2 py-1 text-[10px] font-mono bg-black/20 border border-carbon/50 rounded text-ash">
                {c}
              </span>
            ))}
          </div>
        )}

        <div className="flex justify-between items-center">
          <div className="text-[10px] text-ash font-mono">
            Section {sectionIdx + 1} of {sections.length}
          </div>
          <button onClick={advanceToNext}
            className="btn-primary">
            {isLastStep ? 'Finish Lesson' : hasCheckpoints ? 'Next' : 'Continue'}
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    )
  }

  // Show checkpoint question
  if (question) {
    return (
      <div className="max-w-3xl mx-auto animate-fade-in">
        <Link to="/learn" className="inline-flex items-center gap-1 text-ash hover:text-chalk text-sm mb-4">
          <ArrowLeft className="w-4 h-4" /> Back to Lessons
        </Link>

        <div className="flex items-center gap-2 mb-4">
          <div className="flex-1 h-1 bg-carbon rounded-full">
            <div className="h-1 bg-red rounded-full" style={{ width: `${(step / totalSteps) * 100}%` }} />
          </div>
          <span className="text-[10px] text-ash font-mono">Checkpoint</span>
        </div>

        <div className="card border-carbon/50">
          <div className="flex items-center gap-2 mb-4">
            <span className="px-2 py-0.5 text-[10px] font-mono bg-red/20 text-red border border-red/30 rounded">{question.type}</span>
            <span className="px-2 py-0.5 text-[10px] font-mono bg-green/10 text-green border border-green/30 rounded">{question.difficulty}</span>
          </div>

          <p className="text-chalk mb-6 leading-relaxed">{question.question}</p>

          {!result && (
            <>
              <textarea value={answer} onChange={e => setAnswer(e.target.value)}
                placeholder="Type your answer..." className="input-field font-mono text-sm h-24 resize-none mb-4"
                onKeyDown={handleKeyDown} />
              <div className="flex gap-3">
                <button onClick={submitAnswer} className="btn-primary">Submit</button>
                <button onClick={() => setShowHint(true)} className="btn-ghost"><Lightbulb className="w-4 h-4" /> Hint</button>
              </div>
              {showHint && question.hints?.[0] && (
                <p className="mt-3 text-xs text-red italic">💡 {question.hints[0]}</p>
              )}
            </>
          )}

          {result && (
            <div className={`mt-4 p-4 rounded-lg border ${result.correct ? 'border-green/50 bg-green/5' : 'border-red/50 bg-red/5'}`}>
              <div className="flex items-center gap-2 mb-2">
                {result.correct
                  ? <CheckCircle className="w-5 h-5 text-green" />
                  : <XCircle className="w-5 h-5 text-red" />}
                <span className="font-medium text-sm">{result.correct ? 'Correct!' : 'Incorrect'}</span>
                {result.xp_awarded > 0 && (
                  <span className="text-xs font-mono text-green ml-auto">+{result.xp_awarded} XP</span>
                )}
              </div>
              <p className="text-xs text-ash mb-2">{result.explanation}</p>
              {!result.correct && (
                <p className="text-xs text-ash">Expected: <code className="text-red font-mono">{result.expected}</code></p>
              )}
              <button onClick={advanceToNext} className="btn-primary mt-4">
                Continue <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>
    )
  }

  // No checkpoint available — skip to lesson complete flow
  return (
    <div className="max-w-3xl mx-auto text-center py-16">
      <p className="text-ash mb-4">All sections read. Ready to complete this lesson?</p>
      <button onClick={completeLesson} className="btn-primary">
        Complete Lesson
        <ChevronRight className="w-4 h-4" />
      </button>
    </div>
  )
}


