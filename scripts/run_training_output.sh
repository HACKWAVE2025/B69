#!/bin/bash

# Script to run model training and show output

cd "$(dirname "$0")/.."
source venv/bin/activate

echo "🚀 Starting Isolation Forest Model Training"
echo "==========================================="
echo ""

# Check if custom dataset exists
if [ -f "data/huggingface_combined.csv" ]; then
    echo "📊 Using Hugging Face dataset..."
    python scripts/train_iforest.py --data_path data/huggingface_combined.csv --target_accuracy 0.75
elif [ -f "data/huggingface_dataset.csv" ]; then
    echo "📊 Using Hugging Face dataset..."
    python scripts/train_iforest.py --data_path data/huggingface_dataset.csv --target_accuracy 0.75
else
    echo "📊 Using synthetic data..."
    python scripts/train_iforest.py --target_accuracy 0.85
fi

echo ""
echo "✅ Training complete!"
echo "Model saved to: ml_engine/models/isolation_forest.pkl"

