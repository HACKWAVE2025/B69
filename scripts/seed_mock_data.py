"""Seed MongoDB with mock network flow data."""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models.database import get_database
import random
from datetime import datetime, timedelta
import time

def generate_mock_flows(count=1000):
    """Generate mock network flow data."""
    flows = []
    base_time = datetime.utcnow() - timedelta(hours=24)
    
    for i in range(count):
        timestamp = (base_time + timedelta(seconds=i*10)).isoformat() + "Z"
        flow = {
            "timestamp": timestamp,
            "src_ip": f"10.10.0.{random.randint(1, 50)}",
            "dst_ip": f"10.20.0.{random.randint(1, 50)}",
            "protocol": random.choice(["TCP", "UDP", "ICMP"]),
            "bytes": random.randint(500, 100000),
            "packets": random.randint(1, 200),
            "duration": round(random.random() * 5, 2),
            "src_port": random.randint(1024, 65535),
            "dst_port": random.randint(1, 65535)
        }
        flows.append(flow)
    
    return flows


def generate_mock_anomalies(count=50):
    """Generate mock anomaly alerts."""
    anomalies = []
    base_time = datetime.utcnow() - timedelta(hours=24)
    
    for i in range(count):
        timestamp = (base_time + timedelta(minutes=i*30)).isoformat() + "Z"
        anomaly = {
            "timestamp": timestamp,
            "src_ip": f"10.10.0.{random.randint(1, 50)}",
            "dst_ip": f"10.20.0.{random.randint(1, 50)}",
            "protocol": random.choice(["TCP", "UDP"]),
            "score": round(random.uniform(0.5, 1.0), 4),
            "model": "isolation_forest",
            "features": {
                "bytes": random.randint(50000, 500000),
                "packets": random.randint(100, 1000),
                "duration": round(random.random() * 2, 2)
            },
            "status": random.choice(["new", "acknowledged", "resolved"])
        }
        anomalies.append(anomaly)
    
    return anomalies


def main():
    """Seed database with mock data."""
    print("🌱 Seeding MongoDB with mock data...")
    
    db = get_database()
    flows_collection = db["flows"]
    anomalies_collection = db["anomalies"]
    
    # Clear existing data (optional - comment out to keep existing data)
    print("🗑️  Clearing existing data...")
    flows_collection.delete_many({})
    anomalies_collection.delete_many({})
    
    # Generate and insert flows
    print("📊 Generating mock flows...")
    flows = generate_mock_flows(1000)
    flows_collection.insert_many(flows)
    print(f"✅ Inserted {len(flows)} flows")
    
    # Generate and insert anomalies
    print("🚨 Generating mock anomalies...")
    anomalies = generate_mock_anomalies(50)
    anomalies_collection.insert_many(anomalies)
    print(f"✅ Inserted {len(anomalies)} anomalies")
    
    print("\n✅ Database seeded successfully!")
    print(f"   Total flows: {flows_collection.count_documents({})}")
    print(f"   Total anomalies: {anomalies_collection.count_documents({})}")


if __name__ == "__main__":
    main()

