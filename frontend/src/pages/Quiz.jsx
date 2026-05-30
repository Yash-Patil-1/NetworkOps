import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { CheckCircle, XCircle, Lightbulb } from 'lucide-react'
import axios from 'axios'

export default function Quiz() {
  const [params] = useSearchParams()
  const topicId = params.get('topic') || 'osi-model'
  const [question, setQuestion] = useState(null)
  const [answer, setAnswer] = useState('')
  const [result, setResult] = useState(null)
  const [showHint, setShowHint] = useState(false)
  const [count, setCount] = useState(0)

  const loadQuestion = () => {
    setResult(null); setAnswer(''); setShowHint(false)
    axios.get(`/api/quiz/next?topic=${topicId}`).then(r => setQuestion(r.data)).catch(() => setQuestion(null))
  }

  useEffect(() => { loadQuestion() }, [topicId])

  const submitAnswer = () => {
    if (!answer.trim() || !question) return
    axios.post('/api/quiz/answer', { question_id: question.id, topic_id: topicId, answer })
      .then(r => { setResult(r.data); setCount(c => c + 1) })
  }

  return (
    <div className="max-w-3xl">
      <h1 className="text-3xl font-bold mb-2">Quiz</h1>
      <p className="text-ash mb-8">Topic: <span className="text-amber">{topicId.replace(/-/g,' ')}</span> · Answered: {count}</p>

      {question ? (
        <div className="card">
          <div className="flex justify-between mb-4">
            <span className="tag-amber">{question.type}</span>
            <span className="tag-green">{question.difficulty}</span>
          </div>

          <p className="text-polar mb-6 leading-relaxed">{question.question}</p>

          {!result && (
            <>
              <textarea value={answer} onChange={e => setAnswer(e.target.value)} placeholder="Type your answer..." className="input-field font-mono text-sm h-24 resize-none mb-4" onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submitAnswer() }}}/>
              <div className="flex gap-3">
                <button onClick={submitAnswer} className="btn-primary">Submit</button>
                <button onClick={() => setShowHint(true)} className="btn-ghost"><Lightbulb className="w-4 h-4"/>Hint</button>
              </div>
              {showHint && question.hints?.[0] && <p className="mt-4 text-xs text-amber italic">💡 {question.hints[0]}</p>}
            </>
          )}

          {result && (
            <div className={`mt-4 p-4 rounded-lg border ${result.correct ? 'border-green/50 bg-green/5' : 'border-[#E74C3C]/50 bg-[#E74C3C]/5'}`}>
              <div className="flex items-center gap-2 mb-2">
                {result.correct ? <CheckCircle className="w-5 h-5 text-green"/> : <XCircle className="w-5 h-5 text-[#E74C3C]"/>}
                <span className="font-medium">{result.correct ? 'Correct!' : 'Incorrect'}</span>
              </div>
              <p className="text-xs text-slate mb-2">{result.explanation}</p>
              {!result.correct && <p className="text-xs text-ash">Expected: <code className="text-amber">{result.expected}</code></p>}
              <button onClick={loadQuestion} className="btn-primary mt-4">Next Question →</button>
            </div>
          )}
        </div>
      ) : (
        <p className="text-ash">No questions available for this topic.</p>
      )}
    </div>
  )
}
