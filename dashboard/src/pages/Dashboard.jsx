import React, { useState, useEffect } from 'react'
import MetricsCard from '../components/MetricsCard'
import AnomalyChart from '../components/AnomalyChart'
import { getBaseline, getTimeSeries, getAlertStats, getFlowStats } from '../services/api'

const Dashboard = () => {
  const [baseline, setBaseline] = useState(null)
  const [timeSeries, setTimeSeries] = useState(null)
  const [alertStats, setAlertStats] = useState(null)
  const [flowStats, setFlowStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  const loadData = async () => {
    try {
      const [baselineData, timeSeriesData, alertStatsData, flowStatsData] = await Promise.all([
        getBaseline(),
        getTimeSeries(24),
        getAlertStats(),
        getFlowStats()
      ])
      
      setBaseline(baselineData)
      setTimeSeries(timeSeriesData)
      setAlertStats(alertStatsData)
      setFlowStats(flowStatsData)
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-500">Loading dashboard...</div>
      </div>
    )
  }

  const flowsChartData = timeSeries?.flows ? {
    labels: timeSeries.flows.map(f => f.time),
    datasets: [
      {
        label: 'Flow Count',
        data: timeSeries.flows.map(f => f.count),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
      }
    ]
  } : null

  const anomaliesChartData = timeSeries?.anomalies ? {
    labels: timeSeries.anomalies.map(a => a.time),
    datasets: [
      {
        label: 'Anomaly Count',
        data: timeSeries.anomalies.map(a => a.count),
        borderColor: 'rgb(239, 68, 68)',
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        fill: true,
      }
    ]
  } : null

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Dashboard</h1>

      {/* Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricsCard
          title="Total Flows"
          value={baseline?.total_flows?.toLocaleString() || '0'}
          subtitle="All time"
          color="blue"
        />
        <MetricsCard
          title="Total Anomalies"
          value={baseline?.total_anomalies?.toLocaleString() || '0'}
          subtitle={`${((baseline?.anomaly_rate || 0) * 100).toFixed(2)}% rate`}
          color="red"
        />
        <MetricsCard
          title="Recent Alerts"
          value={alertStats?.recent_24h || '0'}
          subtitle="Last 24 hours"
          color="yellow"
        />
        <MetricsCard
          title="New Alerts"
          value={alertStats?.new || '0'}
          subtitle="Unacknowledged"
          color="purple"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {flowsChartData && (
          <AnomalyChart
            data={flowsChartData}
            type="line"
            title="Network Flows Over Time"
          />
        )}
        {anomaliesChartData && (
          <AnomalyChart
            data={anomaliesChartData}
            type="line"
            title="Anomalies Detected Over Time"
          />
        )}
      </div>

      {/* Protocol Distribution */}
      {baseline?.protocol_distribution && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Protocol Distribution</h2>
          <div className="grid grid-cols-3 gap-4">
            {Object.entries(baseline.protocol_distribution).map(([protocol, count]) => (
              <div key={protocol} className="text-center">
                <p className="text-2xl font-bold text-gray-800">{count.toLocaleString()}</p>
                <p className="text-gray-600">{protocol}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Top Sources & Destinations */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Top Source IPs</h2>
          <ul className="space-y-2">
            {baseline?.top_sources?.slice(0, 5).map((item, idx) => (
              <li key={idx} className="flex justify-between">
                <span className="text-gray-700">{item.ip}</span>
                <span className="font-semibold">{item.count}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4">Top Destination IPs</h2>
          <ul className="space-y-2">
            {baseline?.top_destinations?.slice(0, 5).map((item, idx) => (
              <li key={idx} className="flex justify-between">
                <span className="text-gray-700">{item.ip}</span>
                <span className="font-semibold">{item.count}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

