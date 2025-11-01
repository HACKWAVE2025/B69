# 📊 Custom Dataset Guide for NetSage ML

## Overview

When you provide a custom dataset to the training script, the system automatically detects the format and extracts features accordingly. Here's what happens:

## Supported Dataset Formats

### Option 1: Flow Data Format (Recommended)

**Format:** Raw network flow records similar to what your Kafka producer generates.

**Required Columns:**
- `bytes` (integer) - Number of bytes transferred
- `packets` (integer) - Number of packets
- `duration` (float) - Duration in seconds
- `protocol` (string) - TCP, UDP, or ICMP (optional but recommended)
- `src_port` (integer) - Source port (optional but recommended)
- `dst_port` (integer) - Destination port (optional but recommended)

**Optional Columns:**
- `label` or `anomaly` - 0 for normal, 1 for anomaly (for supervised training)

**Example CSV:**
```csv
bytes,packets,duration,protocol,src_port,dst_port,label
10240,50,2.3,TCP,54321,80,0
500000,800,0.1,TCP,49152,443,1
2048,15,1.5,UDP,55000,53,0
```

**What Happens:**
1. ✅ System detects flow format automatically
2. ✅ Uses `FeatureExtractor` to extract 8 features (same as real-time processing)
3. ✅ Features include: bytes, packets, duration, protocol encoding, bytes_per_packet, normalized ports, flow_rate
4. ✅ If labels exist, trains with evaluation metrics
5. ✅ If no labels, trains in unsupervised mode

### Option 2: Pre-Extracted Features Format

**Format:** CSV with already-extracted numerical features.

**Required Columns:**
- `bytes` (numeric)
- `packets` (numeric)
- `duration` (numeric)

**Optional Columns:**
- Additional numeric columns (up to 8 will be used)
- `label` or `anomaly` - 0 for normal, 1 for anomaly

**Example CSV:**
```csv
bytes,packets,duration,feature4,feature5,feature6,feature7,feature8,label
10240,50,2.3,0.5,0.8,0.3,1024,0
500000,800,0.1,0.9,0.1,0.9,5000,1
```

**What Happens:**
1. ✅ Uses the specified numeric columns directly
2. ✅ If labels exist, trains with evaluation
3. ✅ If no labels, trains in unsupervised mode

## How to Use Custom Dataset

### Method 1: Pass CSV path to training script

```bash
python scripts/train_iforest.py --data_path /path/to/your/data.csv
```

### Method 2: Modify the training script

Edit `scripts/train_iforest.py`:
```python
from ml_engine.train_model import train_isolation_forest

if __name__ == "__main__":
    train_isolation_forest(
        data_path="data/my_custom_dataset.csv",
        target_accuracy=0.85
    )
```

### Method 3: Direct Python call

```python
from ml_engine.train_model import train_isolation_forest

train_isolation_forest(data_path="my_dataset.csv", target_accuracy=0.85)
```

## What Happens During Training

### With Labels (Supervised Mode)

If your CSV has a `label` or `anomaly` column:

1. **Data Loading:** CSV is loaded and analyzed
2. **Feature Extraction:** Features are extracted using the same pipeline as production
3. **Train/Test Split:** 80% train, 20% test (stratified)
4. **Hyperparameter Tuning:** Grid search across 160 combinations
5. **Model Selection:** Best model based on accuracy + F1-score
6. **Evaluation:** Full metrics report including:
   - Accuracy
   - Precision
   - Recall
   - F1-Score
   - Confusion Matrix
   - Classification Report
7. **Model Save:** Best model saved to `ml_engine/models/isolation_forest.pkl`

**Example Output:**
```
📂 Loading custom dataset from: data/my_flows.csv
   Loaded 10000 rows, 7 columns
   Columns: bytes, packets, duration, protocol, src_port, dst_port, label
   📊 Detected flow data format - extracting features using FeatureExtractor...
   ✅ Extracted 10000 feature vectors with 8 features
   📊 Found labels: 200 anomalies, 9800 normal
📊 Train set: 8000 samples
📊 Test set: 2000 samples

🔍 Starting hyperparameter tuning...
...

📈 Test Set Metrics:
   Accuracy:  0.9500 (95.00%)
   Precision: 0.9200 (92.00%)
   Recall:    0.6500 (65.00%)
   F1-Score:  0.7500 (75.00%)
```

### Without Labels (Unsupervised Mode)

If your CSV has NO `label` or `anomaly` column:

1. **Data Loading:** CSV is loaded and analyzed
2. **Feature Extraction:** Features extracted as above
3. **Training:** Model trained on all data (no train/test split)
4. **Hyperparameter Tuning:** Uses default contamination parameters
5. **Model Save:** Model saved without evaluation metrics

**Example Output:**
```
📂 Loading custom dataset from: data/my_flows.csv
   Loaded 10000 rows, 6 columns
   Columns: bytes, packets, duration, protocol, src_port, dst_port
   📊 Detected flow data format - extracting features using FeatureExtractor...
   ✅ Extracted 10000 feature vectors with 8 features
   ⚠️  No labels found - training in unsupervised mode
📊 Training on 10000 samples (unsupervised)
...
```

## Important Notes

1. **Feature Consistency:** When using flow format, the same `FeatureExtractor` is used as in production, ensuring consistency.

2. **Label Format:** 
   - Use `label` column with values: 0 (normal) or 1 (anomaly)
   - OR use `anomaly` column with boolean or 0/1 values

3. **Missing Values:** Rows with missing required fields will be skipped during feature extraction.

4. **Data Size:** 
   - Minimum recommended: 1000 samples
   - Optimal: 10,000+ samples
   - Large datasets (>100k samples) may take longer to train

5. **Model Compatibility:** Models trained on custom datasets are fully compatible with the production Kafka pipeline.

## Example: Creating a Sample Dataset

### From MongoDB (if you've collected flows)

```python
from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb://localhost:27017")
db = client["netsage_ml"]
flows = db["flows"].find()

df = pd.DataFrame(list(flows))
df.to_csv("my_training_data.csv", index=False)
```

### From Kafka Consumer Logs

Export flows from your Kafka consumer or use the seed script:
```bash
python scripts/seed_mock_data.py
# Then export from MongoDB
```

## Troubleshooting

### Error: "Missing required columns"
- Ensure your CSV has at least: `bytes`, `packets`, `duration`
- Or provide all numeric columns for direct feature extraction

### Warning: "No labels found"
- This is normal for unsupervised training
- Model will still train but won't show accuracy metrics
- For evaluation, add a `label` column with 0/1 values

### Model Accuracy Lower Than Expected
- Check if your dataset has enough anomalies (recommended: 2-5% contamination)
- Ensure feature distributions match your production data
- Try adjusting the contamination parameter in `.env`

## Best Practices

1. ✅ Use flow format for consistency with production
2. ✅ Include labels if you have ground truth data
3. ✅ Ensure dataset represents your actual network traffic patterns
4. ✅ Include both normal and anomalous samples when possible
5. ✅ Validate feature distributions match production data

