# 📊 MongoDB Database Guide

## Why You Don't See the Database

**MongoDB only shows databases that contain data!**

By default, MongoDB's `listDatabases` command only shows databases that have at least one collection with data. Empty databases (no collections or no documents) are not displayed.

The `netsage_ml` database is created **automatically** when the first document is inserted.

## Database Structure

### Database Name: `netsage_ml`

**Collections:**
- `flows` - Network flow records
- `anomalies` - Detected anomaly alerts

## How to Populate the Database

### Option 1: Seed Mock Data (Quick Start)

```bash
cd netsage-ml
source venv/bin/activate
python scripts/seed_mock_data.py
```

This creates:
- 1,000 sample flows
- 50 sample anomalies

### Option 2: Run Kafka Pipeline (Real-time Data)

Start the services:

```bash
# Terminal 1: Kafka Producer (sends data)
python kafka/producer.py

# Terminal 2: Kafka Consumer (processes data → MongoDB)
python kafka/consumer.py
```

The consumer automatically:
- Stores all flows in `flows` collection
- Stores detected anomalies in `anomalies` collection

### Option 3: Check if Services Are Running

If Kafka consumer is running, it should be inserting data. Check logs for:
```
✅ Loaded model from ml_engine/models/isolation_forest.pkl
🎯 Kafka consumer started. Listening to topic: network_flows
🔄 Processing flows through ML pipeline...
```

## Viewing the Database

### Using MongoDB Shell (mongosh)

```bash
# Connect to database
mongosh netsage_ml

# List collections
show collections

# Count documents
db.flows.countDocuments({})
db.anomalies.countDocuments({})

# View sample documents
db.flows.findOne()
db.anomalies.findOne()

# Query specific data
db.flows.find({src_ip: "10.10.0.25"}).limit(5)
db.anomalies.find({status: "new"}).limit(5)
```

### Using Python

```python
from api.models.database import get_database

db = get_database()

# Count documents
flow_count = db.flows.count_documents({})
anomaly_count = db.anomalies.count_documents({})

print(f"Flows: {flow_count}")
print(f"Anomalies: {anomaly_count}")

# Query documents
flows = list(db.flows.find().limit(5))
anomalies = list(db.anomalies.find({"status": "new"}).limit(5))
```

### Using MongoDB Compass (GUI)

1. Download MongoDB Compass: https://www.mongodb.com/products/compass
2. Connect to: `mongodb://localhost:27017`
3. Select database: `netsage_ml`
4. Browse collections: `flows` and `anomalies`

## Collection Schemas

### `flows` Collection

```json
{
  "_id": ObjectId("..."),
  "timestamp": "2025-11-01T12:00:00Z",
  "src_ip": "10.10.0.25",
  "dst_ip": "10.20.0.10",
  "protocol": "TCP",
  "bytes": 2048,
  "packets": 15,
  "duration": 2.3,
  "src_port": 54321,
  "dst_port": 80
}
```

### `anomalies` Collection

```json
{
  "_id": ObjectId("..."),
  "timestamp": "2025-11-01T12:00:00Z",
  "src_ip": "10.10.0.25",
  "dst_ip": "10.20.0.10",
  "protocol": "TCP",
  "score": 0.85,
  "model": "isolation_forest",
  "features": {
    "bytes": 50000,
    "packets": 100,
    "duration": 0.5
  },
  "status": "new"
}
```

## Troubleshooting

### Database Not Visible

**Problem:** Database doesn't appear in `listDatabases()`

**Solution:**
1. Insert at least one document:
   ```bash
   python scripts/seed_mock_data.py
   ```
2. Database will appear automatically

### No Data in Collections

**Problem:** Collections exist but are empty

**Possible Causes:**
1. Kafka consumer not running
2. Kafka producer not sending data
3. MongoDB connection issue

**Solution:**
1. Check Kafka consumer is running: `python kafka/consumer.py`
2. Check Kafka producer is running: `python kafka/producer.py`
3. Verify MongoDB is running: `mongosh --eval "db.version()"`
4. Check `.env` file has correct `MONGO_URI`

### Connection Errors

**Problem:** "Connection refused" or "Cannot connect to MongoDB"

**Solution:**
1. Verify MongoDB is running:
   ```bash
   brew services list  # macOS
   # OR
   sudo systemctl status mongod  # Linux
   ```
2. Check connection string in `.env`:
   ```
   MONGO_URI=mongodb://localhost:27017/netsage_ml
   ```
3. Test connection:
   ```bash
   mongosh mongodb://localhost:27017/netsage_ml
   ```

## Quick Commands Reference

```bash
# Seed database with sample data
python scripts/seed_mock_data.py

# Check database via Python
python -c "from api.models.database import get_database; db = get_database(); print('Flows:', db.flows.count_documents({})); print('Anomalies:', db.anomalies.count_documents({}))"

# View via mongosh
mongosh netsage_ml --eval "db.flows.countDocuments({}); db.anomalies.countDocuments({})"

# Clear all data (if needed)
mongosh netsage_ml --eval "db.flows.deleteMany({}); db.anomalies.deleteMany({})"
```

## Expected Data Flow

1. **Kafka Producer** → Sends flow events to Kafka topic
2. **Kafka Consumer** → 
   - Receives flows from Kafka
   - Extracts features using FeatureExtractor
   - Runs ML model (Isolation Forest)
   - Stores flows in `flows` collection
   - Stores anomalies in `anomalies` collection
3. **FastAPI** → Reads from MongoDB collections
4. **Dashboard** → Displays data via FastAPI endpoints

---

**Remember:** The database is created automatically when you insert the first document! 🎉

