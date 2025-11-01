"""Prepare Hugging Face dataset for NetSage ML training."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()


def download_and_convert_dataset(dataset_name="pyToshka/network-intrusion-detection", output_path=None):
    """
    Download dataset from Hugging Face and convert to CSV format.
    
    Args:
        dataset_name: Hugging Face dataset identifier
        output_path: Path to save CSV file (default: data/huggingface_dataset.csv)
    """
    print("=" * 60)
    print("📥 Downloading Dataset from Hugging Face")
    print("=" * 60)
    print(f"Dataset: {dataset_name}\n")
    
    try:
        # Load dataset
        print("🔽 Loading dataset...")
        ds = load_dataset(dataset_name)
        print(f"✅ Dataset loaded successfully!")
        
        # Check available splits
        print(f"\n📊 Available splits: {list(ds.keys())}")
        
        # Use train split if available, otherwise use first available split
        split_name = "train" if "train" in ds else list(ds.keys())[0]
        print(f"📂 Using split: {split_name}")
        
        dataset = ds[split_name]
        print(f"📈 Total samples: {len(dataset)}")
        
        # Convert to pandas DataFrame
        print("\n🔄 Converting to DataFrame...")
        df = dataset.to_pandas()
        
        # Display dataset info
        print(f"\n📋 Dataset Info:")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {len(df.columns)}")
        print(f"   Column names: {list(df.columns)[:10]}...")  # Show first 10
        
        # Try to map columns to NetSage format
        print("\n🔍 Analyzing dataset structure...")
        
        # Common column name mappings (expanded)
        column_mapping = {
            # Flow features
            'bytes': ['bytes', 'byte_count', 'total_bytes', 'Bytes', 'Byte_Count', 'bytes_in', 'bytes_out', 
                     'flow_bytes', 'total_flow_bytes', 'packet_bytes', 'total_packet_bytes'],
            'packets': ['packets', 'packet_count', 'total_packets', 'Packets', 'Packet_Count', 
                       'packets_in', 'packets_out', 'flow_packets', 'total_flow_packets'],
            'duration': ['duration', 'duration_sec', 'time', 'Duration', 'Time', 'flow_duration', 
                        'duration_ms', 'flow_time', 'time_delta', 'timestamp_delta', 'session_duration'],
            'protocol': ['protocol', 'Protocol', 'proto', 'Proto', 'IP_Protocol', 'app_proto'],
            'src_port': ['src_port', 'source_port', 'Src_Port', 'Source_Port', 'srcport'],
            'dst_port': ['dst_port', 'destination_port', 'Dst_Port', 'Dest_Port', 'dest_port', 'dstport'],
            'src_ip': ['src_ip', 'source_ip', 'Src_IP', 'Source_IP'],
            'dst_ip': ['dst_ip', 'destination_ip', 'Dst_IP', 'Dest_IP', 'dest_ip'],
            # Labels
            'label': ['label', 'Label', 'labels', 'Labels'],
            'anomaly': ['anomaly', 'Anomaly', 'attack', 'Attack', 'intrusion', 'Intrusion', 'type', 'event_type'],
        }
        
        # Find matching columns
        available_columns = df.columns.tolist()
        mapped_df = pd.DataFrame()
        found_mappings = {}
        
        for target_col, possible_names in column_mapping.items():
            for col in available_columns:
                if col.lower() in [name.lower() for name in possible_names] or col in possible_names:
                    mapped_df[target_col] = df[col]
                    found_mappings[target_col] = col
                    print(f"   ✅ '{col}' -> '{target_col}'")
                    break
        
        # If we have numeric columns that could be features, include them
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        
        # Check if we have the minimum required columns
        required_cols = ['bytes', 'packets', 'duration']
        missing_required = [col for col in required_cols if col not in mapped_df.columns]
        
        if missing_required:
            print(f"\n⚠️  Warning: Missing required columns: {missing_required}")
            print("   Attempting to generate synthetic values from available data...")
            
            # Try to generate synthetic values based on available data
            # If we have ports or other numeric data, we can create reasonable defaults
            
            if 'bytes' not in mapped_df.columns:
                # Generate synthetic bytes based on port ranges or other heuristics
                # Use a combination of src_port and dst_port if available to create variation
                if 'src_port' in mapped_df.columns and 'dst_port' in mapped_df.columns:
                    # Create bytes estimate: port values * scaling factor
                    mapped_df['bytes'] = (mapped_df['src_port'].abs() + mapped_df['dst_port'].abs()) * 100
                    print(f"   🔄 Generated 'bytes' from port values")
                else:
                    # Use a random distribution similar to normal network traffic
                    import numpy as np
                    mapped_df['bytes'] = np.random.randint(500, 100000, size=len(df))
                    print(f"   🔄 Generated synthetic 'bytes' values")
            
            if 'packets' not in mapped_df.columns:
                # Generate packets based on bytes if available
                if 'bytes' in mapped_df.columns:
                    # Estimate packets: bytes / average packet size
                    mapped_df['packets'] = (mapped_df['bytes'] / 1024).astype(int).clip(1, 200)
                    print(f"   🔄 Generated 'packets' from bytes")
                else:
                    import numpy as np
                    mapped_df['packets'] = np.random.randint(1, 200, size=len(df))
                    print(f"   🔄 Generated synthetic 'packets' values")
            
            if 'duration' not in mapped_df.columns:
                # Generate duration
                import numpy as np
                mapped_df['duration'] = np.random.uniform(0.1, 5.0, size=len(df))
                print(f"   🔄 Generated synthetic 'duration' values")
            
            # Fix zero durations (replace 0.0 with random values)
            if 'duration' in mapped_df.columns:
                zero_durations = (mapped_df['duration'] == 0.0).sum()
                if zero_durations > 0:
                    import numpy as np
                    mask = mapped_df['duration'] == 0.0
                    mapped_df.loc[mask, 'duration'] = np.random.uniform(0.1, 5.0, size=mask.sum())
                    print(f"   🔄 Fixed {zero_durations} zero duration values")
            
            # Remove any remaining missing required columns
            missing_required = [col for col in required_cols if col not in mapped_df.columns]
        
        # Process anomaly column if it exists (convert to label)
        if 'anomaly' in mapped_df.columns:
            # Check if it's already numeric or needs conversion
            if mapped_df['anomaly'].dtype == 'object' or mapped_df['anomaly'].dtype.name == 'category':
                unique_values = [v for v in mapped_df['anomaly'].unique() if pd.notna(v)]
                if len(unique_values) > 0:
                    # Create mapping: flow/normal = 0, alert/malicious = 1
                    label_map = {}
                    for val in unique_values:
                        val_str = str(val).lower()
                        if any(term in val_str for term in ['alert', 'attack', 'malicious', 'intrusion', 'anomaly']):
                            label_map[val] = 1
                        else:
                            label_map[val] = 0
                    
                    mapped_df['label'] = mapped_df['anomaly'].map(label_map)
                    # Fill NaN with 0 (normal)
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
            # Try to find label column
            label_candidates = [col for col in available_columns 
                               if any(term in col.lower() for term in ['label', 'class', 'target', 'attack', 'intrusion']) 
                               and col != 'anomaly']
            
            if label_candidates:
                label_col = label_candidates[0]
                # Normalize labels (assuming 0=normal, 1=anomaly)
                labels = df[label_col]
                if labels.dtype == 'object' or labels.dtype.name == 'category':
                    # Convert categorical to numeric
                    unique_labels = labels.unique()
                    if len(unique_labels) == 2:
                        # Binary classification
                        label_map = {unique_labels[0]: 0, unique_labels[1]: 1}
                        mapped_df['label'] = labels.map(label_map)
                        print(f"   ✅ Mapped '{label_col}' to 'label' (binary: {label_map})")
                    else:
                        print(f"   ⚠️  Found label column '{label_col}' with {len(unique_labels)} classes")
                        print(f"      Classes: {list(unique_labels)[:5]}")
                else:
                    mapped_df['label'] = labels
                    print(f"   ✅ Using '{label_col}' as 'label'")
        
        # Fill missing optional columns with defaults
        if 'protocol' not in mapped_df.columns:
            mapped_df['protocol'] = 'TCP'  # Default
            print("   🔄 Added default 'protocol' = 'TCP'")
        
        if 'src_port' not in mapped_df.columns:
            mapped_df['src_port'] = 0
            print("   🔄 Added default 'src_port' = 0")
        
        if 'dst_port' not in mapped_df.columns:
            mapped_df['dst_port'] = 0
            print("   🔄 Added default 'dst_port' = 0")
        
        # Ensure required columns exist and are numeric
        for col in ['bytes', 'packets', 'duration']:
            if col in mapped_df.columns:
                mapped_df[col] = pd.to_numeric(mapped_df[col], errors='coerce')
        
        # Remove rows with missing required data
        initial_rows = len(mapped_df)
        mapped_df = mapped_df.dropna(subset=['bytes', 'packets', 'duration'])
        removed_rows = initial_rows - len(mapped_df)
        
        if removed_rows > 0:
            print(f"\n⚠️  Removed {removed_rows} rows with missing required data")
        
        print(f"\n✅ Prepared dataset: {len(mapped_df)} samples")
        
        # Display sample
        print("\n📋 Sample data (first 3 rows):")
        print(mapped_df.head(3).to_string())
        
        # Save to CSV
        if output_path is None:
            os.makedirs("data", exist_ok=True)
            output_path = "data/huggingface_dataset.csv"
        
        mapped_df.to_csv(output_path, index=False)
        print(f"\n💾 Saved to: {output_path}")
        
        # Summary statistics
        print("\n📊 Dataset Summary:")
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
        print(f"\n❌ Error loading dataset: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure you're logged in: huggingface-cli login")
        print("   2. Check dataset name is correct")
        print("   3. Verify you have access to the dataset")
        raise


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Download and prepare Hugging Face dataset")
    parser.add_argument(
        "--dataset",
        type=str,
        default="pyToshka/network-intrusion-detection",
        help="Hugging Face dataset identifier"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output CSV path (default: data/huggingface_dataset.csv)"
    )
    
    args = parser.parse_args()
    
    try:
        csv_path = download_and_convert_dataset(args.dataset, args.output)
        print("\n" + "=" * 60)
        print("✅ Dataset preparation complete!")
        print("=" * 60)
        print(f"\n📁 CSV file saved to: {csv_path}")
        print(f"\n🚀 Next step: Train the model with this dataset:")
        print(f"   python scripts/train_iforest.py --data_path {csv_path}")
        print()
        
    except Exception as e:
        print(f"\n❌ Failed to prepare dataset: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

