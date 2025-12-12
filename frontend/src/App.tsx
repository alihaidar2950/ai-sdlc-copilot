import { useState, useEffect } from 'react'
import './App.css'

interface ApiStatus {
  app: string
  version: string
  environment: string
  debug: boolean
  timestamp: string
}

function App() {
  const [status, setStatus] = useState<ApiStatus | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/status')
      .then(res => res.json())
      .then(data => setStatus(data))
      .catch(() => setError('Backend not reachable'))
  }, [])

  return (
    <div className="app">
      <h1>🤖 AI SDLC Co-Pilot</h1>
      <p>Automated test case generation, PR review, and defect creation</p>
      
      <div className="status-card">
        <h2>Backend Status</h2>
        {error ? (
          <p className="error">❌ {error}</p>
        ) : status ? (
          <ul>
            <li><strong>App:</strong> {status.app}</li>
            <li><strong>Version:</strong> {status.version}</li>
            <li><strong>Environment:</strong> {status.environment}</li>
            <li><strong>Debug:</strong> {status.debug ? 'Yes' : 'No'}</li>
          </ul>
        ) : (
          <p>Loading...</p>
        )}
      </div>

      <div className="features">
        <h2>Coming Soon</h2>
        <ul>
          <li>📝 Test Case Generation from Requirements</li>
          <li>🔍 Automated PR Review</li>
          <li>🐛 Intelligent Defect Creation</li>
        </ul>
      </div>
    </div>
  )
}

export default App
