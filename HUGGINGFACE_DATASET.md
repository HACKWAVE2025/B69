# 🤗 Using Hugging Face Dataset

## Quick Start

### Step 1: Install Hugging Face CLI and Login

```bash
pip install huggingface_hub

# Login to access the dataset
huggingface-cli login
```

Enter your Hugging Face token when prompted.

### Step 2: Download and Prepare Dataset

```bash
cd netsage-ml
source venv/bin/activate
pip install datasets  # If not already installed

# Download and convert dataset to CSV
python scripts/prepare_huggingface_dataset.py
```

This will:
- ✅ Download `pyToshka/network-intrusion-detection` from Hugging Face
- ✅ Auto-detect and map columns to NetSage ML format
- ✅ Convert to CSV: `data/huggingface_dataset.csv`
- ✅ Display dataset statistics

### Step 3: Train Model with Dataset

**Option A: One-command (download + train):**
```bash
python scripts/train_with_huggingface.py
```

**Option B: Two-step (download separately, then train):**
```bash
# Step 1: Download (already done)
python scripts/prepare_huggingface_dataset.py

# Step 2: Train
python scripts/train_iforest.py --data_path data/huggingface_dataset.csv
```

---

## What Happens Automatically

The script automatically:

1. **Downloads** the dataset from Hugging Face
2. **Maps columns** to NetSage format:
   - Finds bytes, packets, duration, protocol, ports
   - Maps label/attack/anomaly columns
   - Handles missing columns with defaults
3. **Converts** to CSV format
4. **Extracts features** using FeatureExtractor (same as production)
5. **Trains** model with hyperparameter tuning
6. **Evaluates** with accuracy, precision, recall, F1-score

---

## Expected Output

```
============================================================
📥 Downloading Dataset from Hugging Face
============================================================
Dataset: pyToshka/network-intrusion-detection

🔽 Loading dataset...
✅ Dataset loaded successfully!

📊 Available splits: ['train', 'test']
📂 Using split: train
📈 Total samples: 125973

🔄 Converting to DataFrame...
📋 Dataset Info:
   Shape: (125973, 41)
   Columns: 41
   
🔍 Analyzing dataset structure...
   ✅ 'Total_Fwd_Packets' -> 'packets'
   ✅ 'Flow_Bytes/s' -> 'bytes'
   ✅ 'Flow_Duration' -> 'duration'
   ✅ 'Label' -> 'label'
   ...

✅ Prepared dataset: 125973 samples
💾 Saved to: data/huggingface_dataset.csv

📊 Dataset Summary:
   Total samples: 125973
   Labels distribution:
      Normal (0): 98456 (78.1%)
      Anomaly (1): 27517 (21.9%)
```

---

## Customization

### Use Different Dataset

```bash
python scripts/prepare_huggingface_dataset.py \
  --dataset "username/other-dataset-name" \
  --output "data/my_custom_dataset.csv"
```

### Train with Custom Target Accuracy

```bash
python scripts/train_with_huggingface.py --target_accuracy 0.90
```

### Skip Download (Use Existing CSV)

```bash
python scripts/train_with_huggingface.py \
  --skip_download \
  --data_path data/huggingface_dataset.csv
```

---

## Troubleshooting

### Error: "Not logged in"

**Solution:**
```bash
huggingface-cli login
# Enter your token from: https://huggingface.co/settings/tokens
```

### Error: "Dataset not found"

**Solution:**
- Check dataset name is correct
- Verify you have access to the dataset
- Try: `huggingface-cli repo info pyToshka/network-intrusion-detection`

### Error: "Missing required columns"

**Solution:**
The script will try to auto-map columns. If it fails:
1. Check dataset structure: `python -c "from datasets import load_dataset; ds = load_dataset('pyToshka/network-intrusion-detection'); print(ds['train'][0])"`
2. Manually edit the CSV after download
3. Add missing columns with default values

### Warning: "Using default values"

**Solution:**
This is OK! The script adds default values for:
- `protocol`: Defaults to 'TCP'
- `src_port`, `dst_port`: Default to 0

These defaults allow training to proceed, though accuracy may be lower.

---

## Column Mapping Reference

The script looks for these column names (case-insensitive):

| NetSage Column | Possible Source Names |
|---------------|---------------------|
| `bytes` | bytes, byte_count, total_bytes, Bytes, Flow_Bytes/s |
| `packets` | packets, packet_count, total_packets, Packets, Total_Fwd_Packets |
| `duration` | duration, duration_sec, time, Duration, Flow_Duration |
| `protocol` | protocol, Protocol, proto, Proto, IP_Protocol |
| `src_port` | src_port, source_port, Src_Port, Source_Port |
| `dst_port` | dst_port, destination_port, Dst_Port, Dest_Port |
| `label` | label, Label, labels, Labels, Label, attack, Attack |

---

## Next Steps

After training:

1. **Check model performance:**
   - Look at accuracy, precision, recall in output
   - Model saved to: `ml_engine/models/isolation_forest.pkl`

2. **Use in production:**
   - Model is automatically compatible with Kafka pipeline
   - No changes needed to consumer/producer code

3. **Monitor in dashboard:**
   - Start services as usual (see `HOW_TO_RUN.md`)
   - Model will detect anomalies in real-time

---

## Example: Complete Workflow

```bash
# 1. Login to Hugging Face
huggingface-cli login

# 2. Install dependencies (if needed)
pip install datasets

# 3. Download and train in one command
python scripts/train_with_huggingface.py --target_accuracy 0.85

# 4. Check results
# Look for: "✅ Isolation Forest trained and saved"
# Check metrics: Accuracy, Precision, Recall, F1-Score

# 5. Start services (see HOW_TO_RUN.md)
# Model is ready to use!
```

---

Happy training! 🚀

