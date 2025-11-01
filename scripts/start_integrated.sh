#!/bin/bash

# Script to start both backend and frontend for NetSage ML

echo "🚀 Starting NetSage ML - Integrated System"
echo "==========================================="

# Check if we're in the right directory
if [ ! -f "api/main.py" ]; then
    echo "❌ Error: Please run this script from the netsage-ml root directory"
    exit 1
fi

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Check MongoDB
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  Warning: MongoDB doesn't appear to be running"
    echo "   Please start MongoDB before running this script"
fi

# Check if ports are available
if check_port 8000; then
    echo "⚠️  Warning: Port 8000 is already in use"
fi

if check_port 3000; then
    echo "⚠️  Warning: Port 3000 is already in use"
fi

# Start backend
echo ""
echo "📡 Starting Backend (FastAPI) on port 8000..."
cd "$(dirname "$0")/.."
source venv/bin/activate 2>/dev/null || echo "⚠️  Virtual environment not found, using system Python"
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Frontend (React) on port 3000..."
cd dashboard
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers started!"
echo ""
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo "📍 Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

wait

