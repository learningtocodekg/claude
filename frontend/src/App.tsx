import { useState } from 'react'
import axios from 'axios'
import './index.css'

// TypeScript interface for trading insights
interface TradingInsight {
  headline: string
  article_url: string
  stocks: string[]
  recommendation: string
  rationale: string
  summary: string
}

function App() {
  const [insights, setInsights] = useState<TradingInsight[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const runAnalysis = async () => {
    setLoading(true)
    setError(null)
    setInsights([])

    try {
      const response = await axios.post<TradingInsight[]>(
        'http://localhost:8000/analyze'
      )
      setInsights(response.data)
    } catch (err) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail || 'Failed to fetch analysis')
      } else {
        setError('An unexpected error occurred')
      }
    } finally {
      setLoading(false)
    }
  }

  const getRecommendationClass = (recommendation: string): string => {
    const rec = recommendation.toLowerCase()
    if (rec.includes('buy')) return 'recommendation-buy'
    if (rec.includes('sell')) return 'recommendation-sell'
    return 'recommendation-hold'
  }

  const getPrimaryTicker = (stocks: string[]): string => {
    if (stocks.length === 0) return ''
    // Extract ticker from first stock (handle formats like "AAPL" or "Buy AAPL")
    const first = stocks[0].toUpperCase()
    // Remove common words and extract ticker
    return first.replace(/^(BUY|SELL|HOLD)\s*/i, '').trim()
  }

  return (
    <div className="app-container">
      <div className="app-header">
        <h1 className="app-title">AI Trading Insights</h1>
        <p className="app-subtitle">
          Analyze recent business headlines for potential trading opportunities
        </p>
        <button
          className="analyze-button"
          onClick={runAnalysis}
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Run Analysis'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      {loading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <p className="loading-text">
            Fetching headlines and analyzing with AI...
          </p>
        </div>
      )}

      {!loading && insights.length === 0 && !error && (
        <div className="empty-state">
          <p className="empty-state-text">
            Click "Run Analysis" to see trading insights from recent headlines
          </p>
        </div>
      )}

      {insights.length > 0 && (
        <div className="insights-grid">
          {insights.map((insight, index) => {
            const primaryTicker = getPrimaryTicker(insight.stocks)
            const robinhoodUrl = primaryTicker
              ? `https://robinhood.com/us/en/stocks/${primaryTicker}/`
              : '#'

            return (
              <div key={index} className="insight-card">
                <h2 className="card-headline">
                  <a
                    href={insight.article_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {insight.headline}
                  </a>
                </h2>

                <div className="stocks-list">
                  {insight.stocks.map((stock, i) => (
                    <span key={i} className="stock-chip">
                      {stock.toUpperCase()}
                    </span>
                  ))}
                </div>

                <div
                  className={`recommendation-badge ${getRecommendationClass(
                    insight.recommendation
                  )}`}
                >
                  {insight.recommendation}
                </div>

                <div className="card-section">
                  <div className="card-section-title">Rationale:</div>
                  <div className="card-section-content">{insight.rationale}</div>
                </div>

                <div className="card-section">
                  <div className="card-section-title">Summary:</div>
                  <div className="card-section-content">{insight.summary}</div>
                </div>

                {primaryTicker && (
                  <a
                    href={robinhoodUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="robinhood-button"
                  >
                    View on Robinhood
                  </a>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default App

