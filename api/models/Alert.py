"""Pydantic models for alerts."""
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class Alert(BaseModel):
    """Anomaly alert model."""
    timestamp: str
    src_ip: str
    dst_ip: str
    protocol: str
    score: float
    model: str
    features: Optional[Dict] = None
    status: Optional[str] = "new"
    id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }

