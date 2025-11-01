import React, { useState, useEffect } from 'react'
import AlertTable from '../components/AlertTable'
import MetricsCard from '../components/MetricsCard'
import { getAlerts, updateAlertStatus, getAlertStats } from '../services/api'

const Alerts = () => {
  const [alerts, setAlerts] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState('all')
  const [error, setError] = useState(null)

  useEffect(() => {
    loadAlerts()
    loadStats()
    const interval = setInterval(() => {
      loadAlerts()
      loadStats()
    }, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [statusFilter])

  const loadAlerts = async () => {
    try {
      const params = { limit: 100 }
      if (statusFilter !== 'all') {
        params.status = statusFilter
      }
      const data = await getAlerts(params)
      setAlerts(data)
    } catch (error) {
      console.error('Error loading alerts:', error)
      setError(error.message || 'Failed to load alerts.')
    } finally {
      setLoading(false)
    }
  }

  const loadStats = async () => {
    try {
      const data = await getAlertStats()
      setStats(data)
    } catch (error) {
      console.error('Error loading stats:', error)
    }
  }

  const handleStatusChange = async (alertId, newStatus) => {
    try {
      await updateAlertStatus(alertId, newStatus)
      loadAlerts()
      loadStats()
    } catch (error) {
      console.error('Error updating alert status:', error)
      alert('Failed to update alert status')
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-500">Loading alerts...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
          <h3 className="text-red-800 font-semibold mb-2">Error</h3>
          <p className="text-red-600 text-sm">{error}</p>
          <button
            onClick={() => {
              setError(null)
              loadAlerts()
            }}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">Anomaly Alerts</h1>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">All Statuses</option>
          <option value="new">New</option>
          <option value="acknowledged">Acknowledged</option>
          <option value="resolved">Resolved</option>
        </select>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <MetricsCard
            title="Total Alerts"
            value={stats.total}
            color="blue"
          />
          <MetricsCard
            title="New"
            value={stats.new}
            color="red"
          />
          <MetricsCard
            title="Acknowledged"
            value={stats.acknowledged}
            color="yellow"
          />
          <MetricsCard
            title="Resolved"
            value={stats.resolved}
            color="green"
          />
        </div>
      )}

      {/* Alerts Table */}
      <AlertTable alerts={alerts} onStatusChange={handleStatusChange} />
    </div>
  )
}

export default Alerts

