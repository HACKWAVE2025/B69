"""Train model with Hugging Face dataset in one command."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.prepare_huggingface_dataset import download_and_convert_dataset
from ml_engine.train_model import train_isolation_forest
import argparse


def main():
    """Download dataset and train model."""
    parser = argparse.ArgumentParser(description="Download Hugging Face dataset and train model")
    parser.add_argument(
        "--dataset",
        type=str,
        default="pyToshka/network-intrusion-detection",
        help="Hugging Face dataset identifier"
    )
    parser.add_argument(
        "--target_accuracy",
        type=float,
        default=0.85,
        help="Target accuracy threshold (default: 0.85)"
    )
    parser.add_argument(
        "--skip_download",
        action="store_true",
        help="Skip download, use existing CSV file"
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default="data/huggingface_dataset.csv",
        help="Path to dataset CSV (default: data/huggingface_dataset.csv)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 NetSage ML - Hugging Face Dataset Training")
    print("=" * 60)
    print()
    
    # Download and prepare dataset
    if not args.skip_download:
        if os.path.exists(args.data_path):
            print(f"⚠️  CSV file already exists: {args.data_path}")
            response = input("   Download fresh dataset? (y/n): ").lower()
            if response != 'y':
                print("   Using existing dataset...")
                csv_path = args.data_path
            else:
                csv_path = download_and_convert_dataset(args.dataset, args.data_path)
        else:
            csv_path = download_and_convert_dataset(args.dataset, args.data_path)
    else:
        csv_path = args.data_path
        if not os.path.exists(csv_path):
            print(f"❌ Error: Dataset file not found: {csv_path}")
            print("   Remove --skip_download flag to download dataset")
            sys.exit(1)
        print(f"📂 Using existing dataset: {csv_path}")
    
    print("\n" + "=" * 60)
    print("🧠 Training Model")
    print("=" * 60)
    print()
    
    # Train model
    train_isolation_forest(
        data_path=csv_path,
        target_accuracy=args.target_accuracy
    )
    
    print("\n" + "=" * 60)
    print("✅ Training Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

