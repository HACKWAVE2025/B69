import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Alerts API
export const getAlerts = async (params = {}) => {
  const response = await api.get('/api/alerts/', { params })
  return response.data
}

export const getAlert = async (alertId) => {
  const response = await api.get(`/api/alerts/${alertId}`)
  return response.data
}

export const updateAlertStatus = async (alertId, status) => {
  const response = await api.patch(`/api/alerts/${alertId}/status`, null, {
    params: { status }
  })
  return response.data
}

export const getAlertStats = async () => {
  const response = await api.get('/api/alerts/stats/summary')
  return response.data
}

// Flows API
export const getFlows = async (params = {}) => {
  const response = await api.get('/api/flows/', { params })
  return response.data
}

export const getFlowStats = async () => {
  const response = await api.get('/api/flows/stats/summary')
  return response.data
}

// Stats API
export const getBaseline = async () => {
  const response = await api.get('/api/stats/baseline')
  return response.data
}

export const getTimeSeries = async (hours = 24) => {
  const response = await api.get('/api/stats/time-series', {
    params: { hours }
  })
  return response.data
}

export default api

