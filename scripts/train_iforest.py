"""Training script for Isolation Forest model."""
import sys
import os
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_engine.train_model import train_isolation_forest

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Isolation Forest model for anomaly detection")
    parser.add_argument(
        "--data_path",
        type=str,
        default=None,
        help="Path to custom CSV dataset (optional, defaults to synthetic data)"
    )
    parser.add_argument(
        "--target_accuracy",
        type=float,
        default=0.85,
        help="Target accuracy threshold (default: 0.85)"
    )
    
    args = parser.parse_args()
    
    # Train with custom dataset if provided
    train_isolation_forest(
        data_path=args.data_path,
        target_accuracy=args.target_accuracy
    )

