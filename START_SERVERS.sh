#!/bin/bash

echo "🚀 Starting NetSage ML Platform"
echo "================================"
echo ""

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null 2>&1; then
    echo "⚠️  Warning: MongoDB doesn't appear to be running"
    echo "   Start MongoDB first if you want to use database features"
fi

# Start Backend
echo "📡 Starting Backend API (FastAPI) on port 8000..."
cd "$(dirname "$0")"
source venv/bin/activate
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 > /tmp/netsage-backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
echo "   Logs: /tmp/netsage-backend.log"

# Wait for backend to start
sleep 3

# Start Frontend
echo "🎨 Starting Frontend (React) on port 3000..."
cd dashboard
npm run dev > /tmp/netsage-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
echo "   Logs: /tmp/netsage-frontend.log"

echo ""
echo "✅ Servers starting..."
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop (or kill PIDs: $BACKEND_PID $FRONTEND_PID)"

# Wait for interrupt
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

wait

