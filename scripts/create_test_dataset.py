"""Create a test dataset from Hugging Face dataset similar to the training dataset format."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from datasets import load_dataset
from dotenv import load_dotenv
import numpy as np

load_dotenv()


def create_test_dataset(
    dataset_name="pyToshka/network-intrusion-detection",
    output_path="data/huggingface_test_dataset.csv",
    test_size=100,
    random_seed=42
):
    """
    Create a test dataset from Hugging Face dataset.
    
    Args:
        dataset_name: Hugging Face dataset identifier
        output_path: Path to save test CSV file
        test_size: Number of samples for test set (default: 100)
        random_seed: Random seed for reproducibility
    """
    print("=" * 60)
    print("📥 Creating Test Dataset from Hugging Face")
    print("=" * 60)
    print(f"Dataset: {dataset_name}\n")
    
    try:
        # Load dataset
        print("🔽 Loading dataset...")
        ds = load_dataset(dataset_name)
        print(f"✅ Dataset loaded successfully!")
        
        # Check available splits
        print(f"\n📊 Available splits: {list(ds.keys())}")
        
        # Use test split if available, otherwise use train and sample from it
        if "test" in ds:
            print(f"📂 Using test split")
            dataset = ds["test"]
        elif "train" in ds:
            print(f"📂 Using train split and sampling {test_size} samples for test")
            dataset = ds["train"]
            # Sample if dataset is larger than test_size
            if len(dataset) > test_size:
                dataset = dataset.shuffle(seed=random_seed).select(range(test_size))
        else:
            split_name = list(ds.keys())[0]
            print(f"📂 Using split: {split_name}")
            dataset = ds[split_name]
            if len(dataset) > test_size:
                dataset = dataset.shuffle(seed=random_seed).select(range(test_size))
        
        print(f"📈 Total test samples: {len(dataset)}")
        
        # Convert to pandas DataFrame
        print("\n🔄 Converting to DataFrame...")
        df = dataset.to_pandas()
        
        # Display dataset info
        print(f"\n📋 Dataset Info:")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {len(df.columns)}")
        
        # Map columns to NetSage format (same as training script)
        print("\n🔍 Mapping columns to NetSage format...")
        
        column_mapping = {
            'bytes': ['bytes', 'byte_count', 'total_bytes', 'Bytes', 'Flow_Bytes/s'],
            'packets': ['packets', 'packet_count', 'total_packets', 'Packets', 'Total_Fwd_Packets'],
            'duration': ['duration', 'duration_sec', 'time', 'Duration', 'Flow_Duration', 'session_duration'],
            'protocol': ['protocol', 'Protocol', 'proto', 'Proto', 'IP_Protocol', 'app_proto'],
            'src_port': ['src_port', 'source_port', 'Src_Port', 'Source_Port', 'srcport'],
            'dst_port': ['dst_port', 'destination_port', 'Dst_Port', 'Dest_Port', 'dest_port', 'dstport'],
            'src_ip': ['src_ip', 'source_ip', 'Src_IP', 'Source_IP'],
            'dst_ip': ['dst_ip', 'destination_ip', 'Dst_IP', 'Dest_IP', 'dest_ip'],
            'label': ['label', 'Label', 'labels', 'Labels'],
            'anomaly': ['anomaly', 'Anomaly', 'attack', 'Attack', 'intrusion', 'Intrusion', 'type', 'event_type'],
        }
        
        # Find matching columns
        available_columns = df.columns.tolist()
        mapped_df = pd.DataFrame()
        
        for target_col, possible_names in column_mapping.items():
            for col in available_columns:
                if col.lower() in [name.lower() for name in possible_names] or col in possible_names:
                    mapped_df[target_col] = df[col]
                    print(f"   ✅ '{col}' -> '{target_col}'")
                    break
        
        # Generate missing required columns
        if 'bytes' not in mapped_df.columns:
            if 'src_port' in mapped_df.columns and 'dst_port' in mapped_df.columns:
                mapped_df['bytes'] = (mapped_df['src_port'].abs() + mapped_df['dst_port'].abs()) * 100
                print(f"   🔄 Generated 'bytes' from port values")
            else:
                np.random.seed(random_seed)
                mapped_df['bytes'] = np.random.randint(500, 100000, size=len(df))
                print(f"   🔄 Generated synthetic 'bytes' values")
        
        if 'packets' not in mapped_df.columns:
            if 'bytes' in mapped_df.columns:
                mapped_df['packets'] = (mapped_df['bytes'] / 1024).astype(int).clip(1, 200)
                print(f"   🔄 Generated 'packets' from bytes")
            else:
                np.random.seed(random_seed)
                mapped_df['packets'] = np.random.randint(1, 200, size=len(df))
                print(f"   🔄 Generated synthetic 'packets' values")
        
        if 'duration' not in mapped_df.columns:
            np.random.seed(random_seed)
            mapped_df['duration'] = np.random.uniform(0.1, 5.0, size=len(df))
            print(f"   🔄 Generated synthetic 'duration' values")
        else:
            # Fix zero durations
            zero_durations = (mapped_df['duration'] == 0.0).sum()
            if zero_durations > 0:
                np.random.seed(random_seed)
                mask = mapped_df['duration'] == 0.0
                mapped_df.loc[mask, 'duration'] = np.random.uniform(0.1, 5.0, size=mask.sum())
                print(f"   🔄 Fixed {zero_durations} zero duration values")
        
        # Process anomaly column if it exists (convert to label)
        if 'anomaly' in mapped_df.columns:
            if mapped_df['anomaly'].dtype == 'object' or mapped_df['anomaly'].dtype.name == 'category':
                unique_values = [v for v in mapped_df['anomaly'].unique() if pd.notna(v)]
                if len(unique_values) > 0:
                    label_map = {}
                    for val in unique_values:
                        val_str = str(val).lower()
                        if any(term in val_str for term in ['alert', 'attack', 'malicious', 'intrusion', 'anomaly']):
                            label_map[val] = 1
                        else:
                            label_map[val] = 0
                    
                    mapped_df['label'] = mapped_df['anomaly'].map(label_map)
                    mapped_df['label'] = mapped_df['label'].fillna(0).astype(int)
                    print(f"   ✅ Converted 'anomaly' to 'label' (mapping: {label_map})")
                else:
                    mapped_df['label'] = 0
                    print(f"   ⚠️  'anomaly' column has no valid values, setting all to 0 (normal)")
            else:
                mapped_df['label'] = mapped_df['anomaly'].fillna(0).astype(int)
                print(f"   ✅ Using 'anomaly' as 'label' (already numeric)")
        
        # Add label if not yet created
        if 'label' not in mapped_df.columns:
            label_candidates = [col for col in available_columns 
                               if any(term in col.lower() for term in ['label', 'class', 'target', 'attack', 'intrusion']) 
                               and col != 'anomaly']
            
            if label_candidates:
                label_col = label_candidates[0]
                labels = df[label_col]
                if labels.dtype == 'object' or labels.dtype.name == 'category':
                    unique_labels = labels.unique()
                    if len(unique_labels) == 2:
                        label_map = {unique_labels[0]: 0, unique_labels[1]: 1}
                        mapped_df['label'] = labels.map(label_map)
                        print(f"   ✅ Mapped '{label_col}' to 'label' (binary: {label_map})")
                else:
                    mapped_df['label'] = labels
                    print(f"   ✅ Using '{label_col}' as 'label'")
            else:
                # No labels found, create synthetic labels (80% normal, 20% anomaly)
                np.random.seed(random_seed)
                n_anomalies = int(len(mapped_df) * 0.2)
                labels = np.zeros(len(mapped_df))
                anomaly_indices = np.random.choice(len(mapped_df), n_anomalies, replace=False)
                labels[anomaly_indices] = 1
                mapped_df['label'] = labels.astype(int)
                print(f"   🔄 Generated synthetic labels ({n_anomalies} anomalies, {len(mapped_df)-n_anomalies} normal)")
        
        # Fill missing optional columns with defaults
        if 'protocol' not in mapped_df.columns:
            mapped_df['protocol'] = 'TCP'
            print("   🔄 Added default 'protocol' = 'TCP'")
        
        if 'src_port' not in mapped_df.columns:
            mapped_df['src_port'] = 0
            print("   🔄 Added default 'src_port' = 0")
        
        if 'dst_port' not in mapped_df.columns:
            mapped_df['dst_port'] = 0
            print("   🔄 Added default 'dst_port' = 0")
        
        if 'src_ip' not in mapped_df.columns:
            mapped_df['src_ip'] = f"10.0.0.{np.random.randint(1, 255, size=len(df))}"
            print("   🔄 Added synthetic 'src_ip'")
        
        if 'dst_ip' not in mapped_df.columns:
            mapped_df['dst_ip'] = f"10.0.0.{np.random.randint(1, 255, size=len(df))}"
            print("   🔄 Added synthetic 'dst_ip'")
        
        # Ensure required columns are numeric
        for col in ['bytes', 'packets', 'duration']:
            if col in mapped_df.columns:
                mapped_df[col] = pd.to_numeric(mapped_df[col], errors='coerce')
        
        # Remove rows with missing required data
        initial_rows = len(mapped_df)
        mapped_df = mapped_df.dropna(subset=['bytes', 'packets', 'duration'])
        removed_rows = initial_rows - len(mapped_df)
        
        if removed_rows > 0:
            print(f"\n⚠️  Removed {removed_rows} rows with missing required data")
        
        # Ensure we have the right columns in the right order
        column_order = ['duration', 'protocol', 'src_port', 'dst_port', 'src_ip', 'dst_ip', 'anomaly', 'bytes', 'packets', 'label']
        existing_cols = [col for col in column_order if col in mapped_df.columns]
        other_cols = [col for col in mapped_df.columns if col not in column_order]
        mapped_df = mapped_df[existing_cols + other_cols]
        
        print(f"\n✅ Prepared test dataset: {len(mapped_df)} samples")
        
        # Display sample
        print("\n📋 Sample data (first 3 rows):")
        print(mapped_df.head(3).to_string())
        
        # Save to CSV
        os.makedirs("data", exist_ok=True)
        mapped_df.to_csv(output_path, index=False)
        print(f"\n💾 Saved to: {output_path}")
        
        # Summary statistics
        print("\n📊 Test Dataset Summary:")
        print(f"   Total samples: {len(mapped_df)}")
        if 'label' in mapped_df.columns:
            label_counts = mapped_df['label'].value_counts()
            print(f"   Labels distribution:")
            for label_val, count in label_counts.items():
                label_name = "Anomaly" if label_val == 1 else "Normal"
                print(f"      {label_name} ({label_val}): {count} ({count/len(mapped_df)*100:.1f}%)")
        
        print(f"\n   Features:")
        for col in ['bytes', 'packets', 'duration']:
            if col in mapped_df.columns:
                print(f"      {col}: min={mapped_df[col].min():.2f}, max={mapped_df[col].max():.2f}, mean={mapped_df[col].mean():.2f}")
        
        return output_path
        
    except Exception as e:
        print(f"\n❌ Error creating test dataset: {e}")
        import traceback
        traceback.print_exc()
        raise


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create test dataset from Hugging Face")
    parser.add_argument(
        "--dataset",
        type=str,
        default="pyToshka/network-intrusion-detection",
        help="Hugging Face dataset identifier"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/huggingface_test_dataset.csv",
        help="Output CSV path (default: data/huggingface_test_dataset.csv)"
    )
    parser.add_argument(
        "--test_size",
        type=int,
        default=100,
        help="Number of test samples (default: 100)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)"
    )
    
    args = parser.parse_args()
    
    try:
        csv_path = create_test_dataset(
            dataset_name=args.dataset,
            output_path=args.output,
            test_size=args.test_size,
            random_seed=args.seed
        )
        
        print("\n" + "=" * 60)
        print("✅ Test dataset creation complete!")
        print("=" * 60)
        print(f"\n📁 Test dataset saved to: {csv_path}")
        print(f"\n🚀 Use this for testing:")
        print(f"   python scripts/train_iforest.py --data_path {csv_path}")
        print()
        
    except Exception as e:
        print(f"\n❌ Failed to create test dataset: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

