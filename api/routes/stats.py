"""API routes for statistics and baselines."""
from fastapi import APIRouter
from datetime import datetime, timedelta
from api.models.database import get_database
from api.models.Baseline import BaselineStats
from collections import Counter

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/baseline", response_model=BaselineStats)
async def get_baseline():
    """Get baseline statistics."""
    db = get_database()
    flows_collection = db["flows"]
    anomalies_collection = db["anomalies"]
    
    # Total counts
    total_flows = flows_collection.count_documents({})
    total_anomalies = anomalies_collection.count_documents({})
    anomaly_rate = (total_anomalies / total_flows) if total_flows > 0 else 0.0
    
    # Top source IPs
    pipeline = [
        {"$group": {"_id": "$src_ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_sources = [{"ip": doc["_id"], "count": doc["count"]} 
                   for doc in flows_collection.aggregate(pipeline)]
    
    # Top destination IPs
    pipeline = [
        {"$group": {"_id": "$dst_ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_destinations = [{"ip": doc["_id"], "count": doc["count"]} 
                        for doc in flows_collection.aggregate(pipeline)]
    
    # Protocol distribution
    pipeline = [
        {"$group": {"_id": "$protocol", "count": {"$sum": 1}}}
    ]
    protocol_dist = {doc["_id"]: doc["count"] 
                     for doc in flows_collection.aggregate(pipeline)}
    
    # Average stats
    pipeline = [
        {"$group": {
            "_id": None,
            "avg_bytes": {"$avg": "$bytes"},
            "avg_packets": {"$avg": "$packets"},
            "avg_duration": {"$avg": "$duration"}
        }}
    ]
    result = list(flows_collection.aggregate(pipeline))
    avg_stats = result[0] if result else {
        "avg_bytes": 0,
        "avg_packets": 0,
        "avg_duration": 0
    }
    
    return BaselineStats(
        total_flows=total_flows,
        total_anomalies=total_anomalies,
        anomaly_rate=round(anomaly_rate, 4),
        top_sources=top_sources,
        top_destinations=top_destinations,
        protocol_distribution=protocol_dist,
        avg_bytes=round(avg_stats.get("avg_bytes", 0), 2),
        avg_packets=round(avg_stats.get("avg_packets", 0), 2),
        avg_duration=round(avg_stats.get("avg_duration", 0), 2)
    )


@router.get("/time-series")
async def get_time_series(hours: int = 24):
    """Get time series data for charts."""
    db = get_database()
    flows_collection = db["flows"]
    anomalies_collection = db["anomalies"]
    
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    
    # Flows over time (grouped by hour)
    pipeline = [
        {"$match": {"timestamp": {"$gte": cutoff_time.isoformat()}}},
        {"$group": {
            "_id": {"$substr": ["$timestamp", 0, 13]},  # Group by hour
            "count": {"$sum": 1},
            "avg_bytes": {"$avg": "$bytes"}
        }},
        {"$sort": {"_id": 1}}
    ]
    flows_series = [
        {
            "time": doc["_id"],
            "count": doc["count"],
            "avg_bytes": round(doc["avg_bytes"], 2)
        }
        for doc in flows_collection.aggregate(pipeline)
    ]
    
    # Anomalies over time
    pipeline = [
        {"$match": {"timestamp": {"$gte": cutoff_time.isoformat()}}},
        {"$group": {
            "_id": {"$substr": ["$timestamp", 0, 13]},
            "count": {"$sum": 1},
            "avg_score": {"$avg": "$score"}
        }},
        {"$sort": {"_id": 1}}
    ]
    anomalies_series = [
        {
            "time": doc["_id"],
            "count": doc["count"],
            "avg_score": round(doc["avg_score"], 4)
        }
        for doc in anomalies_collection.aggregate(pipeline)
    ]
    
    return {
        "flows": flows_series,
        "anomalies": anomalies_series,
        "time_range_hours": hours
    }

