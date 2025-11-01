# 🚀 Quick Run Guide

## Servers Status

The servers should now be starting. Check the following URLs:

### ✅ Access Your Application

1. **Frontend Dashboard:** http://localhost:3000
   - Open this in your browser to see the NetSage ML dashboard

2. **Backend API:** http://localhost:8000
   - API endpoint for the backend service

3. **API Documentation:** http://localhost:8000/docs
   - Interactive API documentation (Swagger UI)

4. **Health Check:** http://localhost:8000/health
   - Check if backend is running and connected to MongoDB

### 📊 Populate Test Data (If Dashboard is Empty)

If you see empty dashboards, run this command to populate MongoDB:

```bash
cd /Users/rishitsharma/Documents/netsage-ml
source venv/bin/activate
python scripts/seed_mock_data.py
```

This creates:
- 1000 mock network flows
- ~50 anomaly alerts
- Statistics for visualization

### 🛑 Stop the Servers

If you need to stop the servers:

1. Find the process IDs:
   ```bash
   ps aux | grep uvicorn
   ps aux | grep vite
   ```

2. Kill the processes:
   ```bash
   kill <PID>
   ```

Or use the provided script:
```bash
./START_SERVERS.sh
# Press Ctrl+C to stop
```

### 🔍 Check Server Logs

Backend logs: `/tmp/netsage-backend.log`
Frontend logs: `/tmp/netsage-frontend.log`

View logs:
```bash
tail -f /tmp/netsage-backend.log
tail -f /tmp/netsage-frontend.log
```

### ⚠️ Troubleshooting

**If servers don't start:**
1. Check if ports 8000 or 3000 are already in use
2. Ensure MongoDB is running (for database features)
3. Make sure all dependencies are installed

**Manual start (if needed):**

Terminal 1:
```bash
cd /Users/rishitsharma/Documents/netsage-ml
source venv/bin/activate
python -m uvicorn api.main:app --reload --port 8000
```

Terminal 2:
```bash
cd /Users/rishitsharma/Documents/netsage-ml/dashboard
npm run dev
```

---

**Your NetSage ML platform should now be running!** 🎉

Open http://localhost:3000 in your browser to get started.

