import { useState, useEffect } from 'react'
import React from 'react'
import './App.css'

// Icons (Simple emoji for now, can be replaced with lucide-react or similar if available, but sticking to text/emoji for simplicity as per current setup)
const Icons = {
  Map: '🗺️',
  Alert: '⚠️',
  Check: '✅',
  Traffic: '🚦',
  Speed: '🚀',
  Search: '🔍',
  Data: '📊',
  Settings: '⚙️'
}

function App() {
  const [road, setRoad] = useState('')
  const [area, setArea] = useState('')
  const [locations, setLocations] = useState({ areas: [], roads: [] })

  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // Animation state for "processing" visual
  const [processingStep, setProcessingStep] = useState(0)

  useEffect(() => {
    // Fetch available locations on mount
    fetch('http://localhost:5000/get_locations')
      .then(res => res.json())
      .then(data => {
        if (data.areas) setLocations(data)
      })
      .catch(console.error)
  }, [])

  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setProcessingStep(prev => (prev + 1) % 4)
      }, 500)
      return () => clearInterval(interval)
    }
  }, [loading])

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!road || !area) return

    setLoading(true)
    setError('')
    setResult(null)
    setProcessingStep(0)

    try {
      const response = await fetch('http://localhost:5000/get_diversion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ closed_road: road, area: area }),
      })

      const data = await response.json()
      if (response.ok) {
        if (data.recommendation && data.recommendation.startsWith('Error')) {
          setError(data.recommendation)
        } else {
          setResult(data)
        }
      } else {
        setError(data.error || 'Unable to generate diversion plan. Please try again.')
      }
    } catch (err) {
      setError('Connection refused. Is the server running?')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      {/* Navbar / Header */}
      <header className="main-header">
        <div className="logo-container">
          <div className="logo-icon">{Icons.Traffic}</div>
          <div className="logo-text">
            <h1>UrbanFlow</h1>
            <span>Smart City Intelligence</span>
          </div>
        </div>
        <nav className="main-nav">
          <a href="#" className="active">Dashboard</a>
          <a href="#">Analytics</a>
          <a href="#">Reports</a>
          <a href="#">Settings</a>
        </nav>
        <div className="user-profile">
          <div className="avatar">AD</div>
        </div>
      </header>

      <main className="main-layout dashboard-layout">
        {/* Left Panel: Control Center */}
        <section className="control-panel">
          <div className="panel-header">
            <h2><span className="icon">{Icons.Settings}</span> Simulation Parameters</h2>
            <p>Configure closure scenarios to analyze network impact.</p>
          </div>

          <form onSubmit={handleSearch} className="simulation-form">
            <div className="form-group">
              <label>Target Zone / Area</label>
              <div className="input-wrapper">
                <span className="input-icon">📍</span>
                <input
                  list="areaOptions"
                  value={area}
                  onChange={(e) => setArea(e.target.value)}
                  placeholder="Select Operational Zone..."
                  disabled={loading}
                />
                <datalist id="areaOptions">
                  {locations.areas.map((a, i) => <option key={i} value={a} />)}
                </datalist>
              </div>
            </div>

            <div className="form-group">
              <label>Affected Artery / Road</label>
              <div className="input-wrapper">
                <span className="input-icon">🛣️</span>
                <input
                  list="roadOptions"
                  value={road}
                  onChange={(e) => setRoad(e.target.value)}
                  placeholder="Select Impacted Road..."
                  disabled={loading}
                />
                <datalist id="roadOptions">
                  {locations.roads.map((r, i) => <option key={i} value={r} />)}
                </datalist>
              </div>
            </div>

            <button type="submit" className="primary-btn" disabled={loading || !road || !area}>
              {loading ? (
                <span className="loading-text">
                  Processing Network Graph {'.'.repeat(processingStep)}
                </span>
              ) : 'Run Simulation'}
            </button>
          </form>

          {/* System Status / Quick Stats */}
          <div className="system-status">
            <h3>System Status</h3>
            <div className="status-item">
              <span className="status-label">API Gateway</span>
              <span className="status-dot online"></span>
              <span className="status-value">Online</span>
            </div>
            <div className="status-item">
              <span className="status-label">Prediction Model</span>
              <span className="status-dot online"></span>
              <span className="status-value">Phi-2 Ready</span>
            </div>
            <div className="status-item">
              <span className="status-label">Data Stream</span>
              <span className="status-dot processing"></span>
              <span className="status-value">Live Ingest</span>
            </div>
          </div>
        </section>

        {/* Right Panel: Intelligence Dashboard */}
        <section className="results-panel">
          {error && (
            <div className="message-card error">
              <div className="icon">{Icons.Alert}</div>
              <div className="text">{error}</div>
            </div>
          )}

          {!result && !loading && !error && (
            <div className="empty-dashboard">
              <div className="empty-content">
                <span className="hero-icon">{Icons.Data}</span>
                <h2>Traffic Intelligence Dashboard</h2>
                <p>Select a zone and road to generate real-time AI diversion strategies.</p>
                <div className="feature-grid">
                  <div className="feature-item">
                    <span>⚡</span>
                    <p>Instant Analysis</p>
                  </div>
                  <div className="feature-item">
                    <span>🧠</span>
                    <p>AI-Powered</p>
                  </div>
                  <div className="feature-item">
                    <span>🛡️</span>
                    <p>Safety First</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {result && (
            <div className="dashboard-content">
              {/* Correction Notice */}
              {result.correction_notice && (
                <div className="message-card correction" style={{ marginBottom: '2rem', background: 'rgba(234, 179, 8, 0.15)', border: '1px solid rgba(234, 179, 8, 0.3)', color: '#fcd34d' }}>
                  <div className="icon">⚠️</div>
                  <div className="text">{result.correction_notice}</div>
                </div>
              )}

              {/* Header metrics */}
              <div className="metrics-grid">
                <div className="metric-card highlight">
                  <div className="metric-icon">{Icons.Speed}</div>
                  <div className="metric-info">
                    <span className="label">Recommended Route Speed</span>
                    <span className="value">
                      {result.diversion_details?.avg_speed ? result.diversion_details.avg_speed.toFixed(1) : 'N/A'} <small>km/h</small>
                    </span>
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-icon">🚗</div>
                  <div className="metric-info">
                    <span className="label">Traffic Volume</span>
                    <span className="value">{result.diversion_details?.traffic_volume || 'High'}</span>
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-icon">📈</div>
                  <div className="metric-info">
                    <span className="label">Congestion Index</span>
                    <span className="value" style={{ color: result.diversion_details?.congestion_level > 80 ? '#ef4444' : '#10b981' }}>
                      {(result.diversion_details?.congestion_level || 0).toFixed(2)}%
                    </span>
                  </div>
                </div>
                <div className="metric-card">
                  <div className="metric-icon">🛡️</div>
                  <div className="metric-info">
                    <span className="label">Safety Score</span>
                    <span className="value" style={{ color: '#10b981' }}>
                      {100 - (result.diversion_details?.incidents || 0) * 10}/100
                    </span>
                  </div>
                </div>
              </div>

              {/* Main Analysis Area */}
              <div className="analysis-grid" style={{ gridTemplateColumns: '1.2fr 1fr' }}>
                <div className="analysis-card main-recommendation">
                  <div className="card-header">
                    <h3>AI Strategic Recommendation</h3>
                    <div className="tag">Phi-2 Analysis</div>
                  </div>
                  <div className="card-body">
                    {result.recommendation.split('\n').map((line, i) => {
                      if (!line.trim()) return null

                      const isCritical = line.includes('🚨') || line.includes('CRITICAL')
                      const isHeader = line.startsWith('**') || line.includes('Strategy') || line.includes('Action')

                      return (
                        <p
                          key={i}
                          className="recommendation-line"
                          style={{
                            color: isCritical ? '#ef4444' : 'inherit',
                            fontWeight: isCritical || isHeader ? 'bold' : 'normal',
                            fontSize: isCritical ? '1.1rem' : 'inherit',
                            marginBottom: '0.5rem'
                          }}
                        >
                          {line.replace(/\*\*/g, '')}
                        </p>
                      )
                    })}
                  </div>
                </div>

                <div className="analysis-card details-view">
                  <div className="card-header">
                    <h3>Comparative Route Analysis</h3>
                  </div>
                  <div className="card-body" style={{ overflowY: 'auto', maxHeight: '400px' }}>
                    {result.all_alternatives && result.all_alternatives.length > 0 ? (
                      <table className="analysis-table" style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
                        <thead>
                          <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', textAlign: 'left' }}>
                            <th style={{ padding: '0.5rem' }}>Road & Area</th>
                            <th style={{ padding: '0.5rem' }}>Congestion</th>
                            <th style={{ padding: '0.5rem' }}>Speed</th>
                          </tr>
                        </thead>
                        <tbody>
                          {result.all_alternatives.map((alt, idx) => (
                            <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                              <td style={{ padding: '0.75rem 0.5rem' }}>
                                <div style={{ fontWeight: idx === 0 ? 'bold' : 'normal', color: idx === 0 ? '#60a5fa' : 'inherit' }}>
                                  {alt.name} {idx === 0 && '⭐'}
                                </div>
                                {alt.is_peripheral && (
                                  <span style={{ fontSize: '0.7rem', background: '#3b82f6', color: 'white', padding: '2px 6px', borderRadius: '4px', marginLeft: '0.5rem' }}>
                                    Peripheral
                                  </span>
                                )}
                              </td>
                              <td style={{ padding: '0.5rem' }}>
                                <span style={{
                                  color: alt.congestion > 80 ? '#f87171' : alt.congestion > 50 ? '#facc15' : '#4ade80',
                                  fontWeight: 'bold'
                                }}>
                                  {alt.congestion}%
                                </span>
                              </td>
                              <td style={{ padding: '0.5rem' }}>{alt.speed.toFixed(1)} km/h</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    ) : (
                      <p style={{ opacity: 0.7, padding: '1rem' }}>No alternative routes data available.</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App

