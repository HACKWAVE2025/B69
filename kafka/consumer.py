"""Kafka consumer that processes network flows through ML pipeline."""
from kafka import KafkaConsumer
import json
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_engine.feature_extractor import FeatureExtractor
from ml_engine.anomaly_detector import AnomalyDetector
from api.models.database import get_database

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "network_flows")
IFOREST_MODEL_PATH = os.getenv("IFOREST_MODEL_PATH", "ml_engine/models/isolation_forest.pkl")


def main():
    """Main consumer loop that processes flows through ML pipeline."""
    # Initialize components
    feature_extractor = FeatureExtractor()
    anomaly_detector = AnomalyDetector()
    
    # Load trained model
    try:
        anomaly_detector.load_model(IFOREST_MODEL_PATH)
        print(f"✅ Loaded model from {IFOREST_MODEL_PATH}")
    except Exception as e:
        print(f"⚠️  Could not load model: {e}")
        print("📝 Please train a model first using: python scripts/train_iforest.py")
        return
    
    # Connect to MongoDB
    db = get_database()
    anomalies_collection = db["anomalies"]
    flows_collection = db["flows"]
    
    # Create Kafka consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True
    )
    
    print(f"🎯 Kafka consumer started. Listening to topic: {KAFKA_TOPIC}")
    print(f"📡 Broker: {KAFKA_BROKER}")
    print("🔄 Processing flows through ML pipeline...\n")
    
    try:
        for message in consumer:
            flow = message.value
            
            # Store raw flow
            flow_doc = {
                "timestamp": flow.get("timestamp"),
                "src_ip": flow.get("src_ip"),
                "dst_ip": flow.get("dst_ip"),
                "protocol": flow.get("protocol"),
                "bytes": flow.get("bytes"),
                "packets": flow.get("packets"),
                "duration": flow.get("duration"),
                "src_port": flow.get("src_port"),
                "dst_port": flow.get("dst_port")
            }
            flows_collection.insert_one(flow_doc)
            
            # Extract features
            features = feature_extractor.extract(flow)
            
            if features is not None:
                # Detect anomaly
                is_anomaly, score = anomaly_detector.detect(features)
                
                if is_anomaly:
                    # Store anomaly alert
                    alert = {
                        "timestamp": flow.get("timestamp"),
                        "src_ip": flow.get("src_ip"),
                        "dst_ip": flow.get("dst_ip"),
                        "protocol": flow.get("protocol"),
                        "score": float(score),
                        "model": "isolation_forest",
                        "features": {
                            "bytes": flow.get("bytes"),
                            "packets": flow.get("packets"),
                            "duration": flow.get("duration")
                        },
                        "status": "new"
                    }
                    anomalies_collection.insert_one(alert)
                    print(f"🚨 ANOMALY DETECTED: {flow['src_ip']} -> {flow['dst_ip']} (score: {score:.4f})")
                else:
                    print(f"✓ Normal flow: {flow['src_ip']} -> {flow['dst_ip']}")
            
    except KeyboardInterrupt:
        print("\n🛑 Consumer stopped.")
    finally:
        consumer.close()


if __name__ == "__main__":
    main()

