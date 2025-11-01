#!/bin/bash

# Script to run model training and display output

cd "$(dirname "$0")"
source venv/bin/activate

echo "🚀 Starting Model Training"
echo "=========================="
echo ""

# Check for custom dataset
if [ -f "data/huggingface_combined.csv" ]; then
    echo "📊 Found Hugging Face dataset - using it for training"
    python scripts/train_iforest.py --data_path data/huggingface_combined.csv --target_accuracy 0.75
elif [ -f "data/huggingface_dataset.csv" ]; then
    echo "📊 Found Hugging Face dataset - using it for training"
    python scripts/train_iforest.py --data_path data/huggingface_dataset.csv --target_accuracy 0.75
else
    echo "📊 Using synthetic data for training"
    python scripts/train_iforest.py --target_accuracy 0.85
fi

echo ""
echo "✅ Training completed!"
echo ""
echo "Model saved to: ml_engine/models/isolation_forest.pkl"
echo ""
echo "To use the trained model, it will be automatically loaded by:"
echo "  - Kafka consumer (ml_engine/anomaly_detector.py)"
echo "  - API endpoints"
echo "  - Real-time anomaly detection pipeline"

