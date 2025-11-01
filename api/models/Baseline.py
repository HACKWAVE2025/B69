"""Pydantic models for baseline statistics."""
from pydantic import BaseModel
from typing import Optional, Dict, List


class BaselineStats(BaseModel):
    """Baseline statistics model."""
    total_flows: int
    total_anomalies: int
    anomaly_rate: float
    top_sources: List[Dict]
    top_destinations: List[Dict]
    protocol_distribution: Dict
    avg_bytes: float
    avg_packets: float
    avg_duration: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_flows": 10000,
                "total_anomalies": 200,
                "anomaly_rate": 0.02,
                "top_sources": [{"ip": "10.10.0.1", "count": 150}],
                "top_destinations": [{"ip": "10.20.0.1", "count": 200}],
                "protocol_distribution": {"TCP": 8000, "UDP": 2000},
                "avg_bytes": 51200.5,
                "avg_packets": 45.2,
                "avg_duration": 2.1
            }
        }

