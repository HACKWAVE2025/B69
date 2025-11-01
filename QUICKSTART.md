# 🚀 NetSage ML Quick Start Guide

## Prerequisites

Before starting, ensure you have:
- **Python 3.9+** installed
- **Node.js 16+** installed
- **MongoDB** running on `localhost:27017`
- **Kafka** running on `localhost:9092` (or update `.env` with your Kafka broker)

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
cd netsage-ml
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration (if needed)
```

### 3. Train Initial ML Model

```bash
python scripts/train_iforest.py
```

This will create `ml_engine/models/isolation_forest.pkl`

### 4. Start Services

Open **4 separate terminal windows**:

#### Terminal 1: FastAPI Backend
```bash
source venv/bin/activate  # Activate virtual environment
python -m uvicorn api.main:app --reload --port 8000
```

Verify: Visit http://localhost:8000/docs

#### Terminal 2: Kafka Consumer (ML Pipeline)
```bash
source venv/bin/activate
python kafka/consumer.py
```

#### Terminal 3: Kafka Producer (Mock Data)
```bash
source venv/bin/activate
python kafka/producer.py
```

#### Terminal 4: React Dashboard
```bash
cd dashboard
npm install  # First time only
npm start    # or: npm run dev
```

Verify: Visit http://localhost:3000

### 5. Seed Mock Data (Optional)

If you want to see the dashboard populated with sample data:

```bash
source venv/bin/activate
python scripts/seed_mock_data.py
```

## 🔍 Verifying Everything Works

1. **Check FastAPI**: http://localhost:8000/health
2. **Check Dashboard**: http://localhost:3000
3. **Check Kafka Producer**: Should see "✅ Sent: ..." messages
4. **Check Kafka Consumer**: Should see flow processing messages
5. **Check MongoDB**: Anomalies should appear in the dashboard

## 🐛 Troubleshooting

### Kafka Connection Issues
- Ensure Kafka is running: `kafka-topics.sh --list --bootstrap-server localhost:9092`
- Create topic if needed: `kafka-topics.sh --create --topic network_flows --bootstrap-server localhost:9092`

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongosh --eval "db.version()"`
- Check connection string in `.env`

### Model Not Found
- Run: `python scripts/train_iforest.py`

### Dashboard Not Loading
- Ensure FastAPI is running on port 8000
- Check browser console for errors
- Verify API proxy in `vite.config.js`

## 📊 Using the System

1. **Dashboard**: View real-time metrics and charts
2. **Alerts Page**: View and manage anomaly alerts
3. **Settings**: Configuration (coming soon)

## 🎯 Next Steps

- Customize ML models in `ml_engine/train_model.py`
- Add real network flow data source
- Integrate with Grafana using MongoDB datasource
- Deploy to production

Happy detecting! 🎉

