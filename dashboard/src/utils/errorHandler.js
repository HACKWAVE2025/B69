/**
 * Error handling utilities for API calls
 */

export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    const { status, data } = error.response;
    console.error(`API Error ${status}:`, data);
    
    switch (status) {
      case 401:
        return 'Authentication required. Please log in again.';
      case 403:
        return 'Access forbidden.';
      case 404:
        return 'Resource not found.';
      case 500:
        return 'Server error. Please try again later.';
      default:
        return data?.message || `Error ${status}: ${data?.detail || 'Unknown error'}`;
    }
  } else if (error.request) {
    // Request made but no response
    console.error('Network error:', error.request);
    return 'Unable to connect to server. Please check if the backend is running.';
  } else {
    // Error in request setup
    console.error('Error:', error.message);
    return error.message || 'An unexpected error occurred.';
  }
};

export const checkApiConnection = async () => {
  try {
    const response = await fetch('http://localhost:8000/health');
    const data = await response.json();
    return { connected: true, data };
  } catch (error) {
    return { connected: false, error: error.message };
  }
};

