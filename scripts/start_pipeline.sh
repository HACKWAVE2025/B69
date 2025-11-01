#!/bin/bash

# Start NetSage ML Pipeline
# This script starts all required services

echo "🚀 Starting NetSage ML Pipeline..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env with your configuration"
fi

# Check if models exist
if [ ! -f "ml_engine/models/isolation_forest.pkl" ]; then
    echo "🧠 Training Isolation Forest model..."
    python scripts/train_iforest.py
fi

echo "✅ All setup complete!"
echo ""
echo "To start services:"
echo "  1. Start FastAPI: python -m uvicorn api.main:app --reload --port 8000"
echo "  2. Start Kafka Consumer: python kafka/consumer.py"
echo "  3. Start Kafka Producer: python kafka/producer.py"
echo "  4. Start React Dashboard: cd dashboard && npm start"

