import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response
      console.error(`API Error ${status}:`, data)
    } else if (error.request) {
      // Request made but no response
      console.error('Network error: Unable to connect to backend')
    } else {
      // Error in request setup
      console.error('Error:', error.message)
    }
    return Promise.reject(error)
  }
)

// Alerts API
export const getAlerts = async (params = {}) => {
  const response = await api.get('/api/alerts', { params })
  return response.data
}

export const getAlert = async (alertId) => {
  const response = await api.get(`/api/alerts/${alertId}`)
  return response.data
}

export const updateAlertStatus = async (alertId, status) => {
  const response = await api.patch(`/api/alerts/${alertId}/status?status=${status}`)
  return response.data
}

export const getAlertStats = async () => {
  const response = await api.get('/api/alerts/stats/summary')
  return response.data
}

// Flows API
export const getFlows = async (params = {}) => {
  const response = await api.get('/api/flows', { params })
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

