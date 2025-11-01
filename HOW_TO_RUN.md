# 🚀 How to Run NetSage ML

## Quick Start (5 Steps)

### Step 1: Setup Environment
```bash
cd netsage-ml

# Activate virtual environment (if not already activated)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate      # Windows

# Install dependencies (if not done)
pip install -r requirements.txt
```

### Step 2: Configure & Train Model
```bash
# Ensure .env file exists
cp .env.example .env

# Train the ML model (creates ml_engine/models/isolation_forest.pkl)
python scripts/train_iforest.py
```

### Step 3: Start MongoDB & Kafka
**Make sure these are running before starting the services:**

```bash
# Check MongoDB
mongosh --eval "db.version()"  # Should show version number

# Check Kafka (if installed locally)
kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Step 4: Start All Services

**Open 4 separate terminal windows/tabs:**

#### Terminal 1: FastAPI Backend (API Server)
```bash
cd netsage-ml
source venv/bin/activate
python -m uvicorn api.main:app --reload --port 8000
```
✅ **Check:** http://localhost:8000/docs

#### Terminal 2: Kafka Consumer (ML Pipeline)
```bash
cd netsage-ml
source venv/bin/activate
python kafka/consumer.py
```
✅ **Check:** Should see "🎯 Kafka consumer started" and processing messages

#### Terminal 3: Kafka Producer (Mock Data Generator)
```bash
cd netsage-ml
source venv/bin/activate
python kafka/producer.py
```
✅ **Check:** Should see "✅ Sent: ..." messages every 0.5 seconds

#### Terminal 4: React Dashboard
```bash
cd netsage-ml/dashboard
npm install  # First time only
npm start    # or: npm run dev
```
✅ **Check:** http://localhost:3000

### Step 5: View Dashboard
Open your browser: **http://localhost:3000**

You should see:
- Real-time network flow metrics
- Anomaly alerts (if any detected)
- Charts and statistics

---

## 🎯 Complete Command Reference

### One-Line Startup (After Initial Setup)

```bash
# Terminal 1 - API
cd netsage-ml && source venv/bin/activate && python -m uvicorn api.main:app --reload --port 8000

# Terminal 2 - Consumer
cd netsage-ml && source venv/bin/activate && python kafka/consumer.py

# Terminal 3 - Producer  
cd netsage-ml && source venv/bin/activate && python kafka/producer.py

# Terminal 4 - Dashboard
cd netsage-ml/dashboard && npm start
```

---

## 📋 Startup Checklist

- [ ] Python virtual environment activated
- [ ] MongoDB running on `localhost:27017`
- [ ] Kafka running on `localhost:9092` (or configure `.env`)
- [ ] Model trained (`ml_engine/models/isolation_forest.pkl` exists)
- [ ] FastAPI running on port 8000
- [ ] Kafka consumer running and processing
- [ ] Kafka producer sending data
- [ ] React dashboard running on port 3000

---

## 🔍 Verify Everything is Working

### 1. Check FastAPI Health
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","database":"connected"}
```

### 2. Check API Docs
Open: http://localhost:8000/docs

### 3. Check Dashboard
Open: http://localhost:3000

### 4. Check Kafka Producer
Terminal 3 should show:
```
✅ Sent: 10.10.0.25 -> 10.20.0.10 (2048 bytes)
✅ Sent: 10.10.0.30 -> 10.20.0.15 (15360 bytes)
```

### 5. Check Kafka Consumer
Terminal 2 should show:
```
✓ Normal flow: 10.10.0.25 -> 10.20.0.10
🚨 ANOMALY DETECTED: 10.10.0.30 -> 10.20.0.15 (score: 0.8500)
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Model file not found"
**Solution:**
```bash
python scripts/train_iforest.py
```

### Issue: "Connection refused" (MongoDB)
**Solution:**
```bash
# Start MongoDB (macOS with Homebrew)
brew services start mongodb-community

# Or check if running
mongosh --eval "db.version()"
```

### Issue: "Connection refused" (Kafka)
**Solution:**
```bash
# Update .env with correct Kafka broker
# Or start Kafka if installed locally
```

### Issue: Dashboard shows "No data"
**Solution:**
```bash
# Make sure Kafka producer is running (Terminal 3)
# Or seed mock data:
python scripts/seed_mock_data.py
```

### Issue: Dashboard can't connect to API
**Solution:**
- Check FastAPI is running on port 8000
- Check browser console for CORS errors
- Verify `vite.config.js` has correct proxy settings

---

## 🎬 Optional: Seed Sample Data

To populate the dashboard with sample data:

```bash
source venv/bin/activate
python scripts/seed_mock_data.py
```

This creates:
- 1,000 sample flows
- 50 sample anomalies

Refresh the dashboard to see the data!

---

## 📊 Service URLs

Once everything is running:

- **React Dashboard**: http://localhost:3000
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Alerts API**: http://localhost:8000/api/alerts/
- **Stats API**: http://localhost:8000/api/stats/baseline

---

## 🔄 Stopping Services

Press `Ctrl+C` in each terminal to stop:
1. Stop producer (Terminal 3)
2. Stop consumer (Terminal 2)  
3. Stop dashboard (Terminal 4)
4. Stop FastAPI (Terminal 1)

---

## 💡 Tips

1. **Run in Background:** Use `tmux` or `screen` to keep services running
2. **Check Logs:** Each service prints status messages
3. **Monitor MongoDB:** Use `mongosh` to query data
4. **Custom Dataset:** See `DATASET_GUIDE.md` for training on your data

---

## 🎉 Success Indicators

You'll know everything is working when:
- ✅ All 4 terminals show running services
- ✅ Dashboard loads at http://localhost:3000
- ✅ Producer shows "✅ Sent: ..." messages
- ✅ Consumer shows flow processing
- ✅ Dashboard displays metrics and charts
- ✅ Anomalies appear in dashboard when detected

Happy detecting! 🚨

