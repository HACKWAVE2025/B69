# 🚀 Running NetSage ML on Localhost

## Quick Start Guide

### Option 1: Using Startup Scripts (Recommended)

**Terminal 1 - Start Backend:**
```bash
cd /Users/rishitsharma/Documents/netsage-ml
chmod +x start_backend.sh
./start_backend.sh
```

**Terminal 2 - Start Frontend:**
```bash
cd /Users/rishitsharma/Documents/netsage-ml
chmod +x start_frontend.sh
./start_frontend.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend (FastAPI):**
```bash
cd /Users/rishitsharma/Documents/netsage-ml
source venv/bin/activate
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend (React/Vite):**
```bash
cd /Users/rishitsharma/Documents/netsage-ml/dashboard
npm install  # First time only
npm run dev
```

## 📍 Access URLs

Once both servers are running:

- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

## ✅ Verify Setup

1. **Check Backend:**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"healthy","database":"connected"}`

2. **Check Frontend:**
   - Open browser: http://localhost:3000
   - Open browser console (F12)
   - Should see no CORS errors
   - Dashboard should load (may show "No data" if database is empty)

## 🗄️ Populate Test Data (Optional)

If you see empty dashboards, populate MongoDB with test data:

```bash
cd /Users/rishitsharma/Documents/netsage-ml
source venv/bin/activate
python scripts/seed_mock_data.py
```

This will create:
- 1000 mock network flows
- ~50 anomaly alerts
- Baseline statistics

## 🛑 Stop Servers

Press `Ctrl+C` in each terminal to stop the servers.

## ⚠️ Troubleshooting

### Port Already in Use
If port 8000 or 3000 is already in use:
```bash
# Find process using port 8000
lsof -ti:8000

# Kill process (replace PID with actual process ID)
kill -9 <PID>

# Or use different ports:
# Backend: uvicorn api.main:app --port 8001
# Frontend: Update vite.config.js port to 3001
```

### MongoDB Not Connected
```bash
# Check if MongoDB is running
pgrep mongod

# Start MongoDB (if installed via Homebrew)
brew services start mongodb-community
```

### Frontend Dependencies Missing
```bash
cd /Users/rishitsharma/Documents/netsage-ml/dashboard
npm install
```

### Backend Dependencies Missing
```bash
cd /Users/rishitsharma/Documents/netsage-ml
source venv/bin/activate
pip install -r requirements.txt
```

## 🎉 Success Indicators

✅ Backend terminal shows: `Uvicorn running on http://0.0.0.0:8000`
✅ Frontend terminal shows: `Local: http://localhost:3000`
✅ Browser shows NetSage ML dashboard
✅ No errors in browser console
✅ API calls return data (check Network tab in DevTools)

---

**Note:** Both servers need to run simultaneously. Keep both terminals open while using the application.

