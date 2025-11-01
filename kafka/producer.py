"""Kafka producer for simulating network flow events."""
from kafka import KafkaProducer
import json
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "network_flows")


def generate_flow():
    """Generate a simulated network flow event."""
    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "src_ip": f"10.10.0.{random.randint(1, 50)}",
        "dst_ip": f"10.20.0.{random.randint(1, 50)}",
        "protocol": random.choice(["TCP", "UDP", "ICMP"]),
        "bytes": random.randint(500, 100000),
        "packets": random.randint(1, 200),
        "duration": round(random.random() * 5, 2),
        "src_port": random.randint(1024, 65535),
        "dst_port": random.randint(1, 65535)
    }


def main():
    """Main producer loop."""
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    print(f"🚀 Kafka producer started. Sending to topic: {KAFKA_TOPIC}")
    print(f"📡 Broker: {KAFKA_BROKER}")
    print("Press Ctrl+C to stop...\n")
    
    try:
        while True:
            flow = generate_flow()
            producer.send(KAFKA_TOPIC, flow)
            print(f"✅ Sent: {flow['src_ip']} -> {flow['dst_ip']} ({flow['bytes']} bytes)")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n🛑 Producer stopped.")
    finally:
        producer.close()


if __name__ == "__main__":
    main()

