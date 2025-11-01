"""Evaluate trained model on test dataset."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import joblib
from ml_engine.feature_extractor import FeatureExtractor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.getenv("IFOREST_MODEL_PATH", "ml_engine/models/isolation_forest.pkl")


def evaluate_model_on_test_data(test_data_path, model_path=None):
    """
    Evaluate trained model on test dataset.
    
    Args:
        test_data_path: Path to test CSV file
        model_path: Path to trained model (default: from env)
    """
    if model_path is None:
        model_path = MODEL_PATH
    
    print("=" * 60)
    print("🧪 Model Evaluation on Test Dataset")
    print("=" * 60)
    print()
    
    # Load test dataset
    print(f"📂 Loading test dataset: {test_data_path}")
    df = pd.read_csv(test_data_path)
    print(f"   Loaded {len(df)} test samples")
    print(f"   Columns: {', '.join(df.columns.tolist())}")
    
    # Check for labels
    if 'label' not in df.columns:
        print("\n❌ Error: Test dataset must have 'label' column")
        return
    
    # Load model
    print(f"\n🔍 Loading model from: {model_path}")
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        print("   Please train a model first: python scripts/train_iforest.py")
        return
    
    model = joblib.load(model_path)
    print("✅ Model loaded successfully")
    
    # Extract features
    print("\n📊 Extracting features from test data...")
    extractor = FeatureExtractor()
    
    flows = df.to_dict('records')
    X_test = []
    y_true = []
    valid_indices = []
    
    for idx, flow in enumerate(flows):
        features = extractor.extract(flow)
        if features is not None:
            X_test.append(features[0])
            y_true.append(df.loc[idx, 'label'])
            valid_indices.append(idx)
    
    X_test = np.array(X_test)
    y_true = np.array(y_true)
    
    print(f"   ✅ Extracted {len(X_test)} feature vectors")
    print(f"   Labels: {np.sum(y_true==1)} anomalies, {np.sum(y_true==0)} normal")
    
    # Predict
    print("\n🔮 Running predictions...")
    predictions = model.predict(X_test)
    # Convert Isolation Forest predictions (-1=anomaly, 1=normal) to (1=anomaly, 0=normal)
    y_pred = (predictions == -1).astype(int)
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    
    # Display results
    print("\n" + "=" * 60)
    print("📈 Test Set Evaluation Results")
    print("=" * 60)
    print(f"\n📊 Metrics:")
    print(f"   Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"   Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"   F1-Score:  {f1:.4f} ({f1*100:.2f}%)")
    
    print(f"\n📋 Classification Report:")
    print(classification_report(y_true, y_pred, target_names=['Normal', 'Anomaly']))
    
    print(f"\n🔢 Confusion Matrix:")
    cm = confusion_matrix(y_true, y_pred)
    print(f"                 Predicted")
    print(f"              Normal  Anomaly")
    print(f"Actual Normal  {cm[0,0]:5d}  {cm[0,1]:5d}")
    print(f"       Anomaly {cm[1,0]:5d}  {cm[1,1]:5d}")
    
    # Per-class breakdown
    print(f"\n📊 Per-Class Breakdown:")
    normal_correct = cm[0, 0]
    normal_total = cm[0, 0] + cm[0, 1]
    anomaly_correct = cm[1, 1]
    anomaly_total = cm[1, 0] + cm[1, 1]
    
    print(f"   Normal detection:  {normal_correct}/{normal_total} ({normal_correct/normal_total*100:.2f}%)")
    print(f"   Anomaly detection:  {anomaly_correct}/{anomaly_total} ({anomaly_correct/anomaly_total*100:.2f}%)")
    
    # Overall assessment
    print(f"\n🎯 Overall Assessment:")
    if accuracy >= 0.85:
        print(f"   ✅ Excellent! Accuracy {accuracy*100:.2f}% meets target (≥85%)")
    elif accuracy >= 0.70:
        print(f"   ⚠️  Good accuracy ({accuracy*100:.2f}%) but below target (85%)")
    else:
        print(f"   ❌ Low accuracy ({accuracy*100:.2f}%). Consider retraining with more data.")
    
    if precision >= 0.80 and recall >= 0.60:
        print(f"   ✅ Good balance between precision and recall")
    elif precision < 0.50:
        print(f"   ⚠️  Low precision - too many false positives")
    elif recall < 0.50:
        print(f"   ⚠️  Low recall - missing too many anomalies")
    
    print("\n" + "=" * 60)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm
    }


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate model on test dataset")
    parser.add_argument(
        "--test_data",
        type=str,
        default="data/huggingface_test_dataset.csv",
        help="Path to test dataset CSV"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Path to model file (default: from .env)"
    )
    
    args = parser.parse_args()
    
    try:
        results = evaluate_model_on_test_data(args.test_data, args.model)
        
        if results:
            print("\n✅ Evaluation complete!")
            
    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

