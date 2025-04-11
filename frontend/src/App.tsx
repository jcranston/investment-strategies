import React, { useState } from 'react'
import PortfolioChart from './components/PortfolioChart'


function App() {
  const [strategy, setStrategy] = useState('daily')
  const [startDate, setStartDate] = useState('2024-01-01')
  const [endDate, setEndDate] = useState('2024-12-31')
  const [tickers, setTickers] = useState('AAPL,MSFT')
  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResults(null)
    try {
      const res = await fetch('http://localhost:8000/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          strategy,
          start_date: startDate,
          end_date: endDate,
          tickers: tickers.split(',').map(t => t.trim()),
        }),
      })
      if (!res.ok) {
        throw new Error(`Error: ${res.statusText}`)
      }
      const data = await res.json()
      setResults(data)
    } catch (err: any) {
      setError(err.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-100 to-slate-200 text-slate-800 font-sans">
      <div className="max-w-3xl mx-auto py-12 px-6">
        <div className="bg-white shadow-xl rounded-xl p-10 border border-slate-200">
          <h1 className="text-3xl font-bold text-center text-blue-700 mb-8 tracking-tight">
            📊 Investment Strategy Simulator
          </h1>

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Strategy</label>
                <select
                  className="w-full px-4 py-2 border border-slate-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  value={strategy}
                  onChange={e => setStrategy(e.target.value)}
                >
                  <option value="daily">Daily</option>
                  <option value="rolling">Rolling</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Tickers</label>
                <input
                  type="text"
                  className="w-full px-4 py-2 border border-slate-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  value={tickers}
                  onChange={e => setTickers(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Start Date</label>
                <input
                  type="date"
                  className="w-full px-4 py-2 border border-slate-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  value={startDate}
                  onChange={e => setStartDate(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">End Date</label>
                <input
                  type="date"
                  className="w-full px-4 py-2 border border-slate-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  value={endDate}
                  onChange={e => setEndDate(e.target.value)}
                />
              </div>
            </div>
            <div className="text-center">
              <button
                type="submit"
                disabled={loading}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium shadow-md hover:bg-blue-700 transition disabled:opacity-60"
              >
                {loading ? 'Running Simulation...' : 'Run Simulation'}
              </button>
            </div>
          </form>

          {error && (
            <div className="mt-6 p-4 bg-red-100 border border-red-300 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}
          {results && (
            <div className="mt-10 bg-slate-50 p-6 rounded-lg border border-slate-200 shadow-sm">
              <h2 className="text-xl font-semibold text-slate-800 mb-4">Results</h2>

              <div className="text-sm text-slate-600 mb-4">
                {results.strategy && <p><strong>Strategy:</strong> {results.strategy}</p>}
                <p><strong>Final Portfolio Value:</strong> ${results.portfolio.at(-1)?.Portfolio.toLocaleString()}</p>
              </div>

              <PortfolioChart data={results.portfolio} />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
