"""API routes for anomaly alerts."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
from api.models.database import get_database
from api.models.Alert import Alert
from bson import ObjectId

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("/", response_model=List[Alert])
async def get_alerts(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    status: Optional[str] = None,
    hours: Optional[int] = Query(None, description="Filter alerts from last N hours")
):
    """
    Get anomaly alerts.
    
    Args:
        limit: Maximum number of alerts to return
        offset: Number of alerts to skip
        status: Filter by status (new, acknowledged, resolved)
        hours: Filter alerts from last N hours
    """
    db = get_database()
    collection = db["anomalies"]
    
    query = {}
    
    if status:
        query["status"] = status
    
    if hours:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        query["timestamp"] = {"$gte": cutoff_time.isoformat()}
    
    cursor = collection.find(query).sort("timestamp", -1).skip(offset).limit(limit)
    alerts = []
    
    for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        alerts.append(Alert(**doc))
    
    return alerts


@router.get("/{alert_id}", response_model=Alert)
async def get_alert(alert_id: str):
    """Get a specific alert by ID."""
    db = get_database()
    collection = db["anomalies"]
    
    try:
        doc = collection.find_one({"_id": ObjectId(alert_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        doc["id"] = str(doc.pop("_id"))
        return Alert(**doc)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid alert ID: {str(e)}")


@router.get("/stats/summary")
async def get_alert_stats():
    """Get summary statistics for alerts."""
    db = get_database()
    collection = db["anomalies"]
    
    total = collection.count_documents({})
    new_count = collection.count_documents({"status": "new"})
    acknowledged_count = collection.count_documents({"status": "acknowledged"})
    resolved_count = collection.count_documents({"status": "resolved"})
    
    # Get alerts from last 24 hours
    cutoff_time = datetime.utcnow() - timedelta(hours=24)
    recent_count = collection.count_documents({
        "timestamp": {"$gte": cutoff_time.isoformat()}
    })
    
    # Average score
    pipeline = [
        {"$group": {
            "_id": None,
            "avg_score": {"$avg": "$score"}
        }}
    ]
    result = list(collection.aggregate(pipeline))
    avg_score = result[0]["avg_score"] if result else 0.0
    
    return {
        "total": total,
        "new": new_count,
        "acknowledged": acknowledged_count,
        "resolved": resolved_count,
        "recent_24h": recent_count,
        "avg_score": round(avg_score, 4)
    }


@router.patch("/{alert_id}/status")
async def update_alert_status(alert_id: str, status: str = Query(..., description="new, acknowledged, or resolved")):
    """Update alert status."""
    if status not in ["new", "acknowledged", "resolved"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be: new, acknowledged, or resolved")
    
    db = get_database()
    collection = db["anomalies"]
    
    try:
        result = collection.update_one(
            {"_id": ObjectId(alert_id)},
            {"$set": {"status": status}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return {"message": f"Alert status updated to {status}", "alert_id": alert_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid alert ID: {str(e)}")

