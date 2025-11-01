"""Pydantic models for flow records."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FlowRecord(BaseModel):
    """Network flow record model."""
    timestamp: str
    src_ip: str
    dst_ip: str
    protocol: str
    bytes: int
    packets: int
    duration: float
    src_port: Optional[int] = None
    dst_port: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }

