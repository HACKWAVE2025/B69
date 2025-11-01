# 📊 Expected Model Training Output

When you run `python scripts/train_iforest.py`, you'll see output like this:

## Example Training Output

```
============================================================
🧠 Training Isolation Forest with Hyperparameter Tuning
============================================================

📊 Generating labeled synthetic data...
   Generated 15500 samples (15000 normal, 500 anomalies)

📊 Train set: 12400 samples
📊 Test set: 3100 samples

🔍 Starting hyperparameter tuning...
   This may take a few minutes...

[1/160] Testing: contamination=0.01, n_estimators=100, max_samples=auto, bootstrap=True
[2/160] Testing: contamination=0.01, n_estimators=100, max_samples=auto, bootstrap=False
[3/160] Testing: contamination=0.01, n_estimators=100, max_samples=256, bootstrap=True
   ✅ New best! Accuracy: 0.8725 (87.25%), F1: 0.6123 (61.23%), Combined: 0.7886

[4/160] Testing: contamination=0.01, n_estimators=100, max_samples=256, bootstrap=False
...
[many iterations]
...
[42/160] Testing: contamination=0.02, n_estimators=200, max_samples=512, bootstrap=True
   ✅ New best! Accuracy: 0.8932 (89.32%), F1: 0.6845 (68.45%), Combined: 0.8234

...
[continues until target accuracy is reached or all combinations tested]
...

============================================================
📊 Final Model Evaluation
============================================================

⚙️  Best Parameters:
   contamination: 0.02
   n_estimators: 200
   max_samples: 512
   bootstrap: True

📈 Test Set Metrics:
   Accuracy:  0.8932 (89.32%)
   Precision: 0.7845 (78.45%)
   Recall:    0.6123 (61.23%)
   F1-Score:  0.6845 (68.45%)

📋 Classification Report:
              precision    recall  f1-score   support

      Normal       0.91      0.95      0.93      3000
     Anomaly       0.78      0.61      0.68       100

    accuracy                           0.89      3100
   macro avg       0.85      0.78      0.81      3100
weighted avg       0.89      0.89      0.89      3100

🔢 Confusion Matrix:
                 Predicted
              Normal  Anomaly
Actual Normal   2850     150
       Anomaly     39      61

✅ Isolation Forest trained and saved to ml_engine/models/isolation_forest.pkl
🎉 Target accuracy of 85.0% achieved!
```

## Key Output Sections

### 1. **Data Loading**
- Shows whether using synthetic data or custom dataset
- Displays number of samples (normal vs anomalies)
- Train/test split information

### 2. **Hyperparameter Tuning Progress**
- Shows current iteration `[X/total]`
- Lists parameters being tested
- Updates when better model is found

### 3. **Best Model Metrics**
- **Accuracy**: Overall correctness percentage
- **Precision**: How many predicted anomalies were actually anomalies
- **Recall**: How many actual anomalies were detected
- **F1-Score**: Harmonic mean of precision and recall

### 4. **Classification Report**
- Detailed breakdown by class (Normal vs Anomaly)
- Shows precision, recall, and F1 for each class

### 5. **Confusion Matrix**
- Shows true positives, false positives, true negatives, false negatives
- Helps understand model errors

## Run Training

To see the actual output, run:

```bash
cd /Users/rishitsharma/Documents/netsage-ml
source venv/bin/activate
python scripts/train_iforest.py
```

Or with custom dataset:

```bash
python scripts/train_iforest.py --data_path data/huggingface_combined.csv --target_accuracy 0.75
```

