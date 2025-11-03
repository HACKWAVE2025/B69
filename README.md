# NetSage ML – Network Anomaly Detection Platform

Real-time network anomaly detection system using Kafka for data streaming, MongoDB for persistence, and Python ML models for behavioral analytics.

## 🧩 Overview

NetSage ML is a real-time system that detects network anomalies using **machine learning only** — no IDS or packet capture tools. It consumes streaming flow/telemetry data via **Kafka**, stores enriched results in **MongoDB**, and visualizes alerts and trends in a **React dashboard**.

## ⚙️ Tech Stack

- **Streaming**: Apache Kafka
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **ML Engine**: scikit-learn + PyOD + TensorFlow (for optional AutoEncoder)
- **Frontend**: React + Tailwind CSS + Chart.js
- **Visualization**: Grafana-ready APIs

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- MongoDB running on localhost:27017
- Kafka running on localhost:9092

### Installation

1. **Clone and setup Python environment:**
```bash
cd netsage-ml
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Setup environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Train initial models:**
```bash
python scripts/train_iforest.py
```

4. **Start MongoDB and Kafka** (if not already running)

5. **Start the FastAPI backend:**
```bash
python -m uvicorn api.main:app --reload --port 8000
```

6. **Start Kafka consumer (ML pipeline):**
```bash
python kafka/consumer.py
```

7. **Start Kafka producer (mock data):**
```bash
python kafka/producer.py
```

8. **Setup and start React dashboard:**
```bash
cd dashboard
npm install
npm start
```

## 📁 Project Structure

```
netsage-ml/
├── kafka/
│   ├── producer.py          # Simulates flow events
│   └── consumer.py          # Feeds ML pipeline
├── ml_engine/
│   ├── feature_extractor.py # Feature engineering
│   ├── anomaly_detector.py  # ML model wrapper
│   ├── models/              # Trained model files
│   └── train_model.py       # Training script
├── api/
│   ├── main.py              # FastAPI app
│   ├── routes/              # API endpoints
│   └── models/              # Pydantic models
├── dashboard/               # React frontend
├── scripts/                 # Utility scripts
└── .env.example
```

## 🧠 ML Models

- **Isolation Forest**: Fast unsupervised anomaly detection
- **DBSCAN**: Clustering-based anomaly detection
- **AutoEncoder**: Deep learning anomaly detector (optional)

## 🌟 Features

✅ 100% ML-based anomaly detection (no IDS or DPI)
✅ Real-time Kafka streaming ingestion
✅ MongoDB storage for alerts & flows
✅ Modular ML architecture (swap models easily)
✅ React dashboard for real-time visualization



