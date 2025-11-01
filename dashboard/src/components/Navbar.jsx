import React from 'react'
import { Link, useLocation } from 'react-router-dom'

const Navbar = () => {
  const location = useLocation()

  const isActive = (path) => {
    return location.pathname === path ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-700 hover:text-blue-600'
  }

  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="text-2xl font-bold text-gray-800">
            NetSage ML
          </Link>
          <div className="flex space-x-6">
            <Link
              to="/"
              className={`font-medium ${isActive('/')}`}
            >
              Dashboard
            </Link>
            <Link
              to="/alerts"
              className={`font-medium ${isActive('/alerts')}`}
            >
              Alerts
            </Link>
            <Link
              to="/settings"
              className={`font-medium ${isActive('/settings')}`}
            >
              Settings
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar

