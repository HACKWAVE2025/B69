"""API routes for network flows."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from api.models.database import get_database
from api.models.FlowRecord import FlowRecord

router = APIRouter(prefix="/api/flows", tags=["flows"])


@router.get("/", response_model=List[FlowRecord])
async def get_flows(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    src_ip: Optional[str] = None,
    dst_ip: Optional[str] = None,
    protocol: Optional[str] = None,
    hours: Optional[int] = Query(None, description="Filter flows from last N hours")
):
    """
    Get network flows.
    
    Args:
        limit: Maximum number of flows to return
        offset: Number of flows to skip
        src_ip: Filter by source IP
        dst_ip: Filter by destination IP
        protocol: Filter by protocol
        hours: Filter flows from last N hours
    """
    db = get_database()
    collection = db["flows"]
    
    query = {}
    
    if src_ip:
        query["src_ip"] = src_ip
    if dst_ip:
        query["dst_ip"] = dst_ip
    if protocol:
        query["protocol"] = protocol.upper()
    if hours:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        query["timestamp"] = {"$gte": cutoff_time.isoformat()}
    
    cursor = collection.find(query).sort("timestamp", -1).skip(offset).limit(limit)
    flows = []
    
    for doc in cursor:
        # Remove MongoDB _id field
        doc.pop("_id", None)
        flows.append(FlowRecord(**doc))
    
    return flows


@router.get("/stats/summary")
async def get_flow_stats():
    """Get summary statistics for flows."""
    db = get_database()
    collection = db["flows"]
    
    total = collection.count_documents({})
    
    # Get flows from last 24 hours
    cutoff_time = datetime.utcnow() - timedelta(hours=24)
    recent_count = collection.count_documents({
        "timestamp": {"$gte": cutoff_time.isoformat()}
    })
    
    # Protocol distribution
    pipeline = [
        {"$group": {
            "_id": "$protocol",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ]
    protocol_dist = {doc["_id"]: doc["count"] for doc in collection.aggregate(pipeline)}
    
    # Average stats
    pipeline = [
        {"$group": {
            "_id": None,
            "avg_bytes": {"$avg": "$bytes"},
            "avg_packets": {"$avg": "$packets"},
            "avg_duration": {"$avg": "$duration"}
        }}
    ]
    result = list(collection.aggregate(pipeline))
    avg_stats = result[0] if result else {
        "avg_bytes": 0,
        "avg_packets": 0,
        "avg_duration": 0
    }
    
    return {
        "total": total,
        "recent_24h": recent_count,
        "protocol_distribution": protocol_dist,
        "avg_bytes": round(avg_stats.get("avg_bytes", 0), 2),
        "avg_packets": round(avg_stats.get("avg_packets", 0), 2),
        "avg_duration": round(avg_stats.get("avg_duration", 0), 2)
    }

